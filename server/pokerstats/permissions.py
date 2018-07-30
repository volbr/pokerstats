from rest_framework.permissions import BasePermission

from .models import Game


class IsOwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if type(obj) == Game:
            return request.user.player in obj.team.players.all()
