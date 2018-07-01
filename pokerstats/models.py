from datetime import timedelta
from enum import Enum

from django.db import models
from django.db.models import Sum, Count, Q, F, Subquery, OuterRef, Value
from django.db.models.signals import post_save
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

COMBINATIONS = ('High Card', 'Pair', 'Two Pairs', 'Three of a Kind', 'Straight',
                'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush')

COMBINATIONS_CHOICES = [(str(i), COMBINATIONS[i - 1]) for i in range(1, len(COMBINATIONS) + 1)]


class ChoicesMixin(object):
    @classmethod
    def choices(cls, humanize=True):  # noinspection PyTypeChecker
        return tuple(
            (_.value, _.name.replace('_', ' ').title() if humanize else _.name)
            for _ in cls
        )


class Combination(ChoicesMixin, Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


class SQCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = models.IntegerField()


class SQSum(Subquery):
    output_field = models.DecimalField()

    @property
    def template(self):
        return f"(SELECT sum({self.col}) FROM (%(subquery)s) _sum)"

    def __init__(self, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.col = col


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teams = models.ManyToManyField('pokerstats.Team', blank=True)
    current_team = models.ForeignKey('pokerstats.Team', null=True, blank=True,
                                     related_name='current_team', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        if not instance.first_name:
            instance.first_name = instance.username.title()
            instance.save()


class Team(models.Model):
    name = models.CharField(max_length=64)
    creator = models.ForeignKey(Player, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.name


class Game(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    init_stake = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    finished = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    best_result = models.ForeignKey(
        'pokerstats.GameResult', related_name='best_result',
        null=True, blank=True, on_delete=models.CASCADE)
    best_combination = models.ForeignKey(
        'pokerstats.Round', related_name='best_game_combination', null=True, blank=True, on_delete=models.CASCADE)
    best_winning = models.ForeignKey(
        'pokerstats.Round', related_name='best_game_winning', null=True, blank=True, on_delete=models.CASCADE)

    def finish(self):
        self.finished = timezone.now()
        self.duration = (self.finished - self.created).total_seconds() // 60
        self.set_best_param('combination')
        self.set_best_param('winning')
        self.set_best_result()
        self.save()

    def get_rounds(self):
        return self.round_set.count() - 1

    def set_best_param(self, param):
        best_result = None
        best = None
        for result in self.gameresult_set.all():
            best_result_player = getattr(result, f'best_{param}')
            if best_result_player is None:
                continue
            val = getattr(best_result_player, param)
            if best is None:
                best = val
            if val and val < best:
                continue
            best_result = result
        round = getattr(best_result, f'best_{param}')
        setattr(self, f'best_{param}', round)

    def set_best_result(self):
        best = None
        for result in self.gameresult_set.all():
            if best is None:
                best = result.profit
            if result.profit < best:
                continue
            self.best_result = result

    def game_stats(self):
        win_total = Round.objects.filter(game=OuterRef('game'), winner=OuterRef('pk'))
        rebuy_total = Rebuy.objects.filter(round__game=OuterRef('game'), player=OuterRef('pk'))
        return self.players.all()\
            .values('user')\
            .annotate(
                username=F('user__first_name'),
                win_total=Coalesce(SQSum('winning', win_total.values('winning')), 0),
                wins=SQCount(win_total.values('pk')),
                rebuy_total=Coalesce(SQSum('amount', rebuy_total.values('amount')), 0),
                rebuys=SQCount(rebuy_total.values('pk')),
                total=F('win_total') - F('rebuy_total'))\
            .order_by(F('total').asc(nulls_first=True), 'win_total')\
            .reverse()

    def __str__(self):
        return str(self.created.strftime('%d/%m/%Y %H:%M'))


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    winning = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    combination = models.SmallIntegerField(choices=Combination.choices(), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.created.strftime('%d/%m/%Y %H:%M'))


class Rebuy(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.player} - {self.amount}'


class GameResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    stake = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rebuy = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    best_combination = models.ForeignKey(
        'pokerstats.Round', related_name='best_player_combination', null=True, blank=True, on_delete=models.CASCADE)
    best_winning = models.ForeignKey(
        'pokerstats.Round', related_name='best_player_winning', null=True, blank=True, on_delete=models.CASCADE)

    def set_best_param(self, param):
        best_round = None
        best = 0
        for round in Round.objects.filter(game=self.game, winner=self.player):
            val = getattr(round, param)
            if val and val < best:
                continue
            best_round = round
        setattr(self, f'best_{param}', best_round)

    def save(self, *args, **kwargs):
        if self.stake:
            self.rebuy = Rebuy.objects.filter(round__game=self.game, player=self.player).aggregate(Sum('amount'))['amount__sum']
            rebuy = self.rebuy if self.rebuy else 0
            self.profit = self.stake - rebuy - self.game.init_stake
            self.set_best_param('winning')
            self.set_best_param('combination')

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.game} - {self.player}'
