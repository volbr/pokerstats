from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Sum, Count, Q, F, Max

from .models import Game, GameResult, Round, RoundResult
from .forms import GameForm, RoundResultFormset


@login_required
def home(request):
    current_game = Game.objects.filter(finished__isnull=True).last()
    if current_game:
        url = reverse('current_game', kwargs={'pk': current_game.pk})
        return HttpResponseRedirect(url)
    players = request.user.player.current_team.player_set.all()
    form = GameForm(players, request.POST or None)
    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.team = request.user.player.current_team
        instance.save()
        form.save_m2m()
        url = reverse('current_game', kwargs={'pk': instance.pk})
        return HttpResponseRedirect(url)

    context = {
        'form': form,
        'games': Game.objects.filter(team=request.user.player.current_team).select_related('best_result')
    }
    return render(request, 'home.html', context)


def get_current_round_results(game):
    current_results = RoundResult.objects.filter(round=game.round_set.last(), win__isnull=True)
    if current_results.count() == game.players.count():
        return current_results
    current_results = []
    round = Round.objects.create(game=game)
    for player in game.players.all():
        current_results.append(RoundResult(player=player, round=round))
    RoundResult.objects.bulk_create(current_results)
    return RoundResult.objects.filter(id__in=[r.id for r in current_results])


@login_required
def finish_game(request, pk):
    game = Game.objects.get(id=pk)
    if request.user.player not in game.players.all():
        raise PermissionDenied
    game.finished = timezone.now()
    game.duration = int((game.finished - game.created).total_seconds())
    game_results = []
    player_results = RoundResult.objects.game_stats(game)
    max_profit = 0
    best_result = None
    for r in player_results:
        profit = r['total'] - game.init_stake
        player = game.players.get(id=r['player'])
        result = GameResult(
            game=game,
            player=player,
            win=r['win_total'],
            rebuy=r['rebuy_total'],
            profit=profit
        )
        game_results.append(result)
        if profit > max_profit:
            best_result = result
    if best_result is not None:
        GameResult.objects.bulk_create(game_results)
        game.best_result = best_result
        game.save()
    else:
        game.delete()
    url = reverse('home')
    return HttpResponseRedirect(url)

@login_required
def current_game(request, pk):
    game = Game.objects.get(id=pk)
    if game.finished:
        # TODO: send message
        return HttpResponseRedirect(reverse('home'))

    url = reverse('current_game', kwargs={'pk': game.pk})
    if request.method == 'POST':
        formset = RoundResultFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
        return HttpResponseRedirect(url)

    winners = RoundResult.objects.game_winners(game)
    stats = RoundResult.objects.game_stats(game)
    current_results = get_current_round_results(game)
    formset = RoundResultFormset(queryset=current_results)
    context = {
        'game': game,
        'winners': winners,
        'stats': stats,
        'formset': formset
    }
    return render(request, 'game.html', context=context)
