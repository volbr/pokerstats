from django.contrib import admin

from . import models


class PlayerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'current_team']

    class Meta:
        model = models.Player


class GameModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'created']

    class Meta:
        model = models.Game


admin.site.register(models.Player, PlayerModelAdmin)
admin.site.register(models.Team)
admin.site.register(models.Game, GameModelAdmin)
admin.site.register(models.Rebuy)
admin.site.register(models.Round)
admin.site.register(models.GameResult)
