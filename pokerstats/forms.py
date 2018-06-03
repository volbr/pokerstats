from django import forms
from django.forms import modelformset_factory

from .models import Game, RoundResult, Player


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['players', 'init_stake']
        labels = {'init_stake': 'Initial Stake'}
        widgets = dict(players=forms.SelectMultiple(attrs=dict(size=7)))

    def __init__(self, players, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = players


class RoundResultForm(forms.ModelForm):

    class Meta:
        model = RoundResult
        empty_permitted = False
        fields = ['id', 'round', 'player', 'win', 'rebuy', 'combination']
        widgets = dict(
            round=forms.HiddenInput(),
            player=forms.HiddenInput(),
            id=forms.HiddenInput(),
        )
        labels = dict({f: '' for f in fields})


RoundResultFormset = modelformset_factory(RoundResult, form=RoundResultForm, extra=0)