from enum import Enum

from django.db import models
from django.db.models import Sum, F, Subquery, OuterRef
from django.db.models.signals import post_save
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone


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
    name = models.CharField(max_length=32)
    teams = models.ManyToManyField('pokerstats.Team', blank=True)
    current_team = models.ForeignKey('pokerstats.Team', null=True, blank=True,
                                     related_name='players', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance, name=instance.username.title())
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
    creator = models.ForeignKey(Player, related_name='game_creator', on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    init_stake = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    finished = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    best_result = models.ForeignKey(
        'pokerstats.GameResult', related_name='best_result_games',
        null=True, blank=True, on_delete=models.CASCADE)
    best_combination = models.ForeignKey(
        'pokerstats.Round', related_name='best_combination_games',
        null=True, blank=True, on_delete=models.CASCADE)
    best_winning = models.ForeignKey(
        'pokerstats.Round', related_name='best_winning_games',
        null=True, blank=True, on_delete=models.CASCADE)

    def finish(self):
        self.finished = timezone.now()
        self.duration = (self.finished - self.created).total_seconds() // 60
        results = self.results.all()
        [self._set_best(results, param) for param in ('combination', 'winning')]
        self._set_best_result(results)
        self.save()

    def get_rounds(self):
        return self.rounds.count() - 1

    def _set_best(self, results, param):
        best_result, best = None, None
        for result in results:
            best_result_player = getattr(result, f'best_{param}')
            if best_result_player is None:
                continue
            val = getattr(best_result_player, param)
            if val is None:
                continue
            if best is None:
                best = val
            if val < best:
                continue
            best_result, best = result, val
        best_round = getattr(best_result, f'best_{param}') if best_result else None
        setattr(self, f'best_{param}', best_round)

    def _set_best_result(self, results):
        best_result, best = None, None
        for result in results:
            if best is None:
                best = result.profit
            if result.profit < best:
                continue
            best_result, best = result, result.profit
        self.best_result = best_result

    def game_stats(self):
        win_total = Round.objects.filter(game=OuterRef('game'), winner=OuterRef('pk'))
        rebuy_total = Rebuy.objects.filter(round__game=OuterRef('game'), player=OuterRef('pk'))
        return self.players.all()\
            .values('user')\
            .annotate(
                username=F('name'),
                win_total=Coalesce(SQSum('winning', win_total.values('winning')), 0),
                wins=SQCount(win_total.values('pk')),
                rebuy_total=Coalesce(SQSum('amount', rebuy_total.values('amount')), 0),
                rebuys=SQCount(rebuy_total.values('pk')),
                total=F('win_total') - F('rebuy_total'))\
            .order_by(F('total').desc(nulls_first=True))


class Round(models.Model):
    game = models.ForeignKey(Game, related_name="rounds", on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    winning = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    combination = models.SmallIntegerField(choices=Combination.choices(), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)


class Rebuy(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)


class GameResult(models.Model):

    game = models.ForeignKey(Game, related_name='results', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    stake = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rebuy = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    best_combination = models.ForeignKey(
        'pokerstats.Round', related_name='best_combination_results',
        null=True, blank=True, on_delete=models.CASCADE)
    best_winning = models.ForeignKey(
        'pokerstats.Round', related_name='best_winning_results',
        null=True, blank=True, on_delete=models.CASCADE)

    def _set_best(self, rounds, param):
        best_round, best = None, None
        for round in rounds:
            val = getattr(round, param)
            if val is None:
                continue
            if best is None:
                best = val
            if val < best:
                continue
            best_round, best = round, val
        setattr(self, f'best_{param}', best_round)

    def save(self, *args, **kwargs):
        if self.stake is not None:
            rebuy = Rebuy.objects.filter(round__game=self.game, player=self.player)\
                .aggregate(Sum('amount'))['amount__sum']
            self.rebuy = rebuy if rebuy is not None else 0
            self.profit = self.stake - self.rebuy - self.game.init_stake
            rounds = Round.objects.filter(game=self.game, winner=self.player)
            [self._set_best(rounds, param) for param in ('combination', 'winning')]

        super().save(*args, **kwargs)
