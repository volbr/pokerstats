from django.contrib import admin

from . import models

admin.site.register(models.Player)
admin.site.register(models.Team)
admin.site.register(models.Game)
admin.site.register(models.Round)
admin.site.register(models.RoundResult)
admin.site.register(models.GameResult)
