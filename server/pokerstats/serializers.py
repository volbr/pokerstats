from .models import Team, Player, Round, Game, GameResult, Rebuy

from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name')


class RebuySerializer(serializers.ModelSerializer):

    class Meta:
        model = Rebuy
        fields = ('round', 'player', 'amount')


class RoundSerializer(serializers.ModelSerializer):

    class Meta:
        model = Round
        fields = ('id', 'winner', 'winning', 'combination')

    winner = serializers.StringRelatedField()
    combination = serializers.SerializerMethodField()

    @staticmethod
    def get_combination(obj):
        return obj.get_combination_display()


class RoundUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Round
        fields = ('id', 'winner', 'winning', 'combination')


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name', 'players')

    players = PlayerSerializer(many=True)


class GameResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameResult
        fields = ('id', 'game', 'player', 'stake', 'rebuy',
                  'profit', 'best_combination', 'best_winning')

    player = PlayerSerializer()
    best_combination = serializers.SerializerMethodField()
    best_winning = serializers.FloatField(source='best_winning.winning', allow_null=True)

    @staticmethod
    def get_best_combination(obj):
        if obj.best_combination:
            return obj.best_combination.get_combination_display()


class GameResultCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameResult
        fields = ('game', 'player', 'stake')


class PlayerExtendedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name', 'team', 'game')

    team = TeamSerializer(source='current_team')
    game = serializers.SerializerMethodField()

    @staticmethod
    def get_game(obj):
        game = obj.game_set.filter(finished__isnull=True).first()
        return game.pk if game else None


class GameCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'players', 'creator', 'init_stake', 'team')
        read_only_fields = ('id',)


class GameWithResultsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'results', 'rounds', 'best_result', 'best_combination',
                  'best_winning', 'created', 'finished')

    results = GameResultSerializer(many=True)
    rounds = serializers.SerializerMethodField()
    best_result = GameResultSerializer()
    best_combination = RoundSerializer()
    best_winning = RoundSerializer()

    @staticmethod
    def get_rounds(obj):
        return obj.get_rounds()


class GameWithRoundsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'creator', 'players', 'rounds', 'stats', 'round', 'created')

    players = PlayerSerializer(many=True)
    rounds = RoundSerializer(many=True)
    stats = serializers.SerializerMethodField()
    round = serializers.SerializerMethodField()

    @staticmethod
    def get_stats(obj):
        return obj.game_stats()

    @staticmethod
    def get_round(obj):
        round, _ = Round.objects.get_or_create(game=obj, winner__isnull=True)
        return round.id if round else None
