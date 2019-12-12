from rest_framework.serializers import ModelSerializer

from app.models import Player, GlobalStats, Game


class PlayerSerializer(ModelSerializer):

    class Meta:
        model = Player
        fields = '__all__'


class GlobalStatsSerializer(ModelSerializer):

    class Meta:
        model = GlobalStats
        fields = ['users', 'date', 'game']


class GameSerializer(ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'
