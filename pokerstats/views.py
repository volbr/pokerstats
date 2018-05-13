from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum, Count, Q, F

from .models import Game, RoundResult
from .forms import GameForm


@login_required
def home(request):
    current_game = Game.objects.filter(finished__isnull=True).last()
    if current_game:
        url = reverse('current_game', kwargs={'pk': current_game.pk})
        return HttpResponseRedirect(url)
    players = request.user.player.current_team.player_set.all()
    game_form = GameForm(players, request.POST or None)
    if request.POST and game_form.is_valid():
        instance = game_form.save(commit=False)
        instance.team = request.user.player.current_team
        instance.save()
        url = reverse('current_game', kwargs={'pk': instance.pk})
        return HttpResponseRedirect(url)
    context = {
        'game_form': game_form
    }
    return render(request, 'home.html', context)


def current_game(request, pk):
    game = Game.objects.get(id=pk)
    base_query = RoundResult.objects.filter(round__game=game).select_related('player__user')
    winners = base_query.filter(win__isnull=False)
    stats = base_query.select_related('player__user')\
        .values('player')\
        .annotate(
            username=F('player__user__username'),
            win_total=Sum('win'),
            rebuy_total=Sum('rebuy'),
            wins=Count('id', filter=Q(win__isnull=False)),
            rebuys=Count('id', filter=Q(rebuy__isnull=False)),
    )
    context = {
        'game': game,
        'winners': winners,
        'stats': stats
    }
    return render(request, 'game.html', context=context)
