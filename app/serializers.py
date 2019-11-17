from rest_framework.serializers import ModelSerializer

from app.models import Player


class PlayerSerializer(ModelSerializer):

    class Meta:
        model = Player
        fields = ['id']
