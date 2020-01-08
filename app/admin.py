from django.contrib import admin
from django.apps import apps

from app.models import GlobalStats, PlayerStats, Player, Game, Achievement, PlayerAchievement, AchievementsOverTime

app = apps.get_app_config('app')


class GameFilter(admin.ModelAdmin):
    list_filter = ('game__name',)


class PlayerAndGameFilter(GameFilter):
    search_fields = ('player__nickname',)


admin.site.register(GlobalStats, GameFilter)
admin.site.register(PlayerStats, PlayerAndGameFilter)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(AchievementsOverTime, PlayerAndGameFilter)
admin.site.register(Achievement, GameFilter)
admin.site.register(PlayerAchievement)

admin.site.site_header = 'Game Stats Analysis'
