from django import forms

from .models import Game, Rebuy, Round, GameResult


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['players', 'init_stake']
        labels = {'init_stake': 'Initial Stake'}
        widgets = dict(players=forms.SelectMultiple(attrs=dict(size=7)))

    def __init__(self, players=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if players:
            self.fields['players'].queryset = players


class RebuyForm(forms.ModelForm):

    class Meta:
        model = Rebuy
        fields = ['player', 'amount', 'round']
        widgets = dict(round=forms.HiddenInput())
        labels = dict({f: '' for f in fields})

    def __init__(self, players=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if players:
            self.fields['player'].queryset = players


class RoundForm(forms.ModelForm):

    class Meta:
        model = Round
        fields = ['winner', 'winning', 'combination', 'game']
        widgets = dict(game=forms.HiddenInput())
        labels = dict({f: '' for f in fields})

    def __init__(self, players=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if players:
            self.fields['winner'].queryset = players


class GameResultForm(forms.ModelForm):

    class Meta:
        model = GameResult
        empty_permitted = False
        fields = ['id', 'game', 'player', 'stake']
        widgets = dict(
            game=forms.HiddenInput(),
            player=forms.HiddenInput(),
            id=forms.HiddenInput(),
        )
        labels = dict({f: '' for f in fields})

GameResultFormset = forms.modelformset_factory(GameResult, form=GameResultForm, extra=0)