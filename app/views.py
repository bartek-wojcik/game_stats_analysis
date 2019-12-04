from django_filters.rest_framework import FilterSet
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from app.models import Player, GlobalStats, Game
from app.serializers import PlayerSerializer, GlobalStatsSerializer, GameSerializer


class PlayerView(CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GlobalStatsViewSet(ModelViewSet):
    queryset = GlobalStats.objects.all()
    serializer_class = GlobalStatsSerializer
    filterset_fields = ('game', )


class GamesViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
