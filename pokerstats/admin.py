from django.contrib import admin

from . import models


class PlayerModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_team']

    class Meta:
        model = models.models

admin.site.register(models.Player, PlayerModelAdmin)
admin.site.register(models.Team)
admin.site.register(models.Game)
admin.site.register(models.Round)
admin.site.register(models.RoundResult)
admin.site.register(models.GameResult)
