from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from app.models import Player, GlobalStats, Game, Achievement, PlayerStats
from app.serializers import PlayerSerializer, GlobalStatsSerializer, GameSerializer, AchievementSerializer, \
    PlayerStatsSerializer


class PlayerView(APIView):

    def get(self, request):
        players = Player.objects.all()
        search_filter = request.query_params.get('search', None)
        if search_filter:
            players = players.filter(nickname__search=search_filter)[:10]
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GlobalStatsView(APIView):

    def get(self, request):
        stats = GlobalStats.objects.all()
        game_filter = request.query_params.get('game', None)
        if game_filter:
            stats = stats.filter(game=game_filter)
        serializer = GlobalStatsSerializer(stats, many=True)
        return Response(serializer.data)


class GamesViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class AchievementView(APIView):

    def get(self, request):
        achievements = Achievement.objects.all()
        game_filter = request.query_params.get('game', None)
        if game_filter:
            achievements = achievements.filter(game=game_filter)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data)


class PlayerStatsView(APIView):

    def get(self, request):
        stats = PlayerStats.objects.all()
        game_filter = request.query_params.get('game', None)
        player_filter = request.query_params.get('player', None)
        if not game_filter or not player_filter:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stats = stats.filter(game=game_filter, player=player_filter)
        serializer = PlayerStatsSerializer(stats, many=True)
        return Response(serializer.data)

