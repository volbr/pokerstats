from django.db import models
from django.db.models import Sum, Count, Q, F
from django.db.models.signals import post_save
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.contrib.auth.models import User


COMBINATIONS = ('High Card', 'Pair', 'Two Pairs', 'Three of a Kind', 'Straight',
                'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush')

COMBINATIONS_CHOICES = [(str(i), COMBINATIONS[i - 1]) for i in range(1, len(COMBINATIONS) + 1)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_team = models.ForeignKey('pokerstats.Team', null=True, blank=True,
                                     related_name='current_team', on_delete=models.CASCADE)
    teams = models.ManyToManyField('pokerstats.Team', blank=True)

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

    def __str__(self):
        return str(self.created.strftime('%d/%m/%Y %H:%M'))


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.created.strftime('%d/%m/%Y %H:%M'))


class RoundResultManager(models.Manager):

    def game_stats(self, game):
        return self.filter(round__game=game)\
            .values('player')\
            .annotate(
                username=F('player__user__first_name'),
                win_total=Coalesce(Sum('win'), 0),
                rebuy_total=Coalesce(Sum('rebuy'), 0),
                wins=Count('id', filter=Q(win__isnull=False)),
                rebuys=Count('id', filter=Q(rebuy__isnull=False)),
                total=F('win_total') - F('rebuy_total'))\
            .order_by(F('total').asc(nulls_first=True), 'win_total')\
            .reverse()

    def game_winners(self, game):
        return self.filter(round__game=game, win__isnull=False).select_related('player__user')


class RoundResult(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    win = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rebuy = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    combination = models.CharField(max_length=16, choices=COMBINATIONS_CHOICES, null=True, blank=True)

    objects = RoundResultManager()

    def __str__(self):
        return f'{self.round} - {self.player}'


class GameResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    win = models.DecimalField(max_digits=6, decimal_places=2)
    rebuy = models.DecimalField(max_digits=6, decimal_places=2)
    profit = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.game} - {self.player}'
