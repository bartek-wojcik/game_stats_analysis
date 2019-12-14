from django.urls import path

from .views import GlobalStatsView, GamesViewSet, AchievementView, PlayerStatsView, PlayerViewSet

urlpatterns = [
    path('players', PlayerViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('globalstats', GlobalStatsView.as_view()),
    path('playerstats', PlayerStatsView.as_view()),
    path('games', GamesViewSet.as_view({'get': 'list'})),
    path('achievements', AchievementView.as_view()),
]