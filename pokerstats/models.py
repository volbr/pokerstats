from django.db import models
from django.contrib.auth.models import User


COMBINATIONS = ('Royal Flush', 'Straight Flush', 'Four of a Kind',
                'Full House', 'Flush', 'Straight', 'Three of a Kind',
                'Two Pairs', 'Pair', 'High Card')


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teams = models.ManyToManyField('pokerstats.Team')


class Team(models.Model):
    name = models.CharField(max_length=64)
    creator = models.ForeignKey(Player)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)


class Game(models.Model):
    team = models.ForeignKey(Team)
    players = models.ManyToManyField(Player)
    winner = models.ForeignKey(Player, null=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    finished = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)


class Round(models.Model):

    COMBINATIONS_CHOICES = [(str(i), COMBINATIONS[i]) for i in range(1, len(COMBINATIONS)+1)]

    game = models.ForeignKey(Game)
    winner = models.ForeignKey(Player)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    combination = models.CharField(max_length=16, choices=COMBINATIONS_CHOICES, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)


class GameResult(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    amount = models.DecimalField(max_digits=6, decimal_places=2)


class BuyChips(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    round = models.ForeignKey(Round, null=True, blank=True)
