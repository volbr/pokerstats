from django.forms import ModelForm

from .models import Game, RoundResult


class GameForm(ModelForm):

    class Meta:
        model = Game
        fields = ['players', 'init_stake']
        labels = {'init_stake': 'Initial Stake'}

    def __init__(self, players, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = players


class RoundResultForm(ModelForm):

    class Meta:
        model = RoundResult
        fields = ['player', 'win', 'rebuy', 'combination']