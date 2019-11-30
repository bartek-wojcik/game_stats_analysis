from rest_framework.serializers import ModelSerializer

from app.models import Player, GlobalStats


class PlayerSerializer(ModelSerializer):

    class Meta:
        model = Player
        fields = ['id']


class GlobalStatsSerializer(ModelSerializer):

    class Meta:
        model = GlobalStats
        fields = '__all__'
