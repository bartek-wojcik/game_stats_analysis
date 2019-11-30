from django.urls import path

from .views import PlayerView, GlobalStatsViewset

urlpatterns = [
    path('player', PlayerView.as_view()),
    path('globalstats', GlobalStatsViewset.as_view({'get': 'list'})),
]