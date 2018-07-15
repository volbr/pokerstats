from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

from .models import Game, GameResult, Round
from .forms import GameForm, RebuyForm, RoundForm, GameResultFormset


@login_required
def home(request):
    players = request.user.player.current_team.player_set.all()
    form = GameForm(players, request.POST or None)
    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.team = request.user.player.current_team
        instance.save()
        form.save_m2m()
        game_results = [GameResult(player=player, game=instance) for player in instance.players.all()]
        GameResult.objects.bulk_create(game_results)
        url = reverse('current_game', kwargs={'pk': instance.pk})
        return HttpResponseRedirect(url)

    current_game = Game.objects.filter(finished__isnull=True).last()
    games = Game.objects.filter(
        team=request.user.player.current_team,
        finished__isnull=False).select_related('best_result')
    context = {
        'form': form,
        'current_game': current_game,
        'games': games
    }
    return render(request, 'home.html', context)


@login_required
def current_game(request, pk):
    game = Game.objects.get(id=pk)
    current_round = game.round_set.count()
    round, _ = Round.objects.get_or_create(game=game, winner__isnull=True)
    players = game.players.all()
    if request.method == 'POST':
        formset = GameResultFormset(request.POST)
        if formset.is_valid():
            formset.save()
            game.finish()
        else:
            print(formset.errors)
        return HttpResponseRedirect(reverse('home'))
    context = {
        'game': game,
        'rounds': Round.objects.filter(game=game, winning__isnull=False).select_related('winner__user'),
        'stats': game.game_stats(),
        'round_form': RoundForm(players, instance=round),
        'rebuy_form': RebuyForm(players, initial={'round': round}),
        'game_formset': GameResultFormset(queryset=GameResult.objects.filter(game=game)),
        'current_round': current_round,
    }
    return render(request, 'current_game.html', context=context)



class GameDetailView(DetailView):

    model = Game
    template_name = 'game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rounds'] = Round.objects.filter(
            game=self.object, winning__isnull=False).select_related('winner__user')
        context['stats'] = self.object.game_stats()
        return context


class RebuyCreate(FormView):
    form_class = RebuyForm

    def form_valid(self, form):
        instance = form.save()
        return HttpResponseRedirect(reverse('current_game', kwargs={'pk': instance.round.game.pk}))

    def form_invalid(self, form):
        print(form.errors)


class RoundUpdate(FormView):
    form_class = RoundForm

    def form_valid(self, form):
        instance = form.save()
        return HttpResponseRedirect(reverse('current_game', kwargs={'pk': instance.game.pk}))

    def form_invalid(self, form):
        print(form.errors)
