from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Game
from .forms import GameForm


@login_required
def home(request):
    current_game = Game.objects.filter(finished__isnull=True).last()
    if current_game:
        url = reverse('current_game', kwargs={'game_pk': current_game.pk})
        return HttpResponseRedirect(url)
    players = request.user.player.current_team.player_set.all()
    game_form = GameForm(players, request.POST or None)
    if request.POST and game_form.is_valid():
        instance = game_form.save()
        url = reverse('current_game', kwargs={'game_pk': instance.pk})
        return HttpResponseRedirect(url)
    context = {
        'game_form': game_form
    }
    return render(request, 'home.html', context)


def current_game(request, game_pk):
    game = Game.objects.get(id=game_pk)
    context = {
        'game': game,
    }
    return render(request, 'game.html', {})
