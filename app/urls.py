from django.urls import path

from .views import PlayerView, GlobalStatsView, GamesViewSet, AchievementView, PlayerStatsView

urlpatterns = [
    path('players', PlayerView.as_view()),
    path('globalstats', GlobalStatsView.as_view()),
    path('playerstats', PlayerStatsView.as_view()),
    path('games', GamesViewSet.as_view({'get': 'list'})),
    path('achievements', AchievementView.as_view()),
]