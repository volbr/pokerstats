from django.db.models import Prefetch
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView, ListAPIView, get_object_or_404, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Player, Game, Round, Rebuy, GameResult
from . import serializers


class PlayerDetailView(RetrieveAPIView):
    serializer_class = serializers.PlayerExtendedSerializer

    def get_object(self):
        return get_object_or_404(Player, user=self.request.user)


class GameCreateView(CreateAPIView):
    serializer_class = serializers.GameCreateSerializer
    queryset = Game.objects.all()


class GameDetailView(RetrieveAPIView):
    serializer_class = serializers.GameWithRoundsSerializer
    queryset = Game.objects.prefetch_related(
        'players',
        Prefetch(
            'rounds',
            queryset=Round.objects.filter(winner__isnull=False).select_related('winner'),
        )
    )


class GameListView(ListAPIView):
    serializer_class = serializers.GameWithResultsSerializer

    def get_queryset(self):
        prefetch_results = GameResult.objects.order_by('player__name').select_related(
            'player', 'best_combination', 'best_winning')
        return Game.objects.filter(
            finished__isnull=False,
            team=self.request.user.player.current_team
        ).select_related(
            'best_result__player',
            'best_result__best_combination',
            'best_result__best_winning',
            'best_combination__winner',
            'best_winning__winner',
        ).prefetch_related(
            Prefetch('results', queryset=prefetch_results),
            'rounds'
        )


class RebuyCreateView(CreateAPIView):
    serializer_class = serializers.RebuySerializer
    queryset = Rebuy.objects.all()


class RoundUpdateView(UpdateAPIView):
    serializer_class = serializers.RoundUpdateSerializer
    queryset = Round.objects.all()


class GameFinishView(APIView):

    def post(self, request):
        if not request.data or type(request.data) is not list:
            return Response({'detail': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        game = get_object_or_404(Game, pk=request.data[0].get('game'))
        if game is None:
            return Response({'detail': 'Bad request: no game provided'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.player.current_team != game.team:
            raise PermissionDenied
        serializer = serializers.GameResultCreateSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            game.finish()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
