from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from app.models import Player, GlobalStats, Game
from app.serializers import PlayerSerializer, GlobalStatsSerializer, GameSerializer


class PlayerView(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nickname']


class GlobalStatsViewSet(ModelViewSet):
    queryset = GlobalStats.objects.all()
    serializer_class = GlobalStatsSerializer
    filterset_fields = ('game', )


class GamesViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
