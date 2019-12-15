from rest_framework.serializers import ModelSerializer

from app.models import Player, GlobalStats, Game, Achievement, PlayerStats, PlayerAchievement


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


class AchievementSerializer(ModelSerializer):

    class Meta:
        model = Achievement
        fields = '__all__'


class PlayerStatsSerializer(ModelSerializer):

    class Meta:
        model = PlayerStats
        fields = '__all__'


class PlayerAchievementSerializer(ModelSerializer):

    class Meta:
        model = PlayerAchievement
        fields = ['achievement', 'achieved']
