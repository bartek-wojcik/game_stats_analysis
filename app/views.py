from rest_framework.generics import CreateAPIView
from app.models import Player
from app.serializers import PlayerSerializer


class PlayerView(CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
