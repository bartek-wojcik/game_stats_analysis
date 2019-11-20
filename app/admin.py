from django.contrib import admin
from django.apps import apps

from app.models import GlobalStats, PlayerStats, Player, Game, Achievement, PlayerAchievement

app = apps.get_app_config('app')


class GameFilter(admin.ModelAdmin):
    list_filter = ('game__name',)


admin.site.register(GlobalStats, GameFilter)
admin.site.register(PlayerStats, GameFilter)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Achievement)
admin.site.register(PlayerAchievement)

admin.site.site_header = 'Game Stats Analysis'
