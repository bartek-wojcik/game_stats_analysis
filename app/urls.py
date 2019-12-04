from django.urls import path

from .views import PlayerView, GlobalStatsViewSet, GamesViewSet

urlpatterns = [
    path('player', PlayerView.as_view()),
    path('globalstats', GlobalStatsViewSet.as_view({'get': 'list'})),
    path('games', GamesViewSet.as_view({'get': 'list'})),
]