from rest_framework.permissions import BasePermission

from .models import Game, Round, Rebuy


class IsOwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        player = request.user.player
        if type(obj) == Game:
            return player in obj.team.players.all()
        elif type(obj) == Round:
            return player.current_team == obj.game.team
        elif type(obj) == Rebuy:
            return player.current_team == obj.round.game.team
        return True
