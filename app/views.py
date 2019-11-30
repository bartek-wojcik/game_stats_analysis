from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from app.models import Player, GlobalStats
from app.serializers import PlayerSerializer, GlobalStatsSerializer


class PlayerView(CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GlobalStatsViewset(ModelViewSet):
    queryset = GlobalStats.objects.all()
    serializer_class = GlobalStatsSerializer
    filterset_fields = ('game', )
