from datetime import timedelta

from django.db.models import Max, F, Count, Case, When
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from app.models import Player, GlobalStats, Game, Achievement, PlayerStats, PlayerAchievement, AchievementsOverTime
from app.serializers import PlayerSerializer, GlobalStatsSerializer, GameSerializer, AchievementSerializer, \
    PlayerStatsSerializer, PlayerAchievementSerializer, AchievementsOverTimeSerializer


class RequiredSearchFilter(SearchFilter):

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)

        if not search_terms:
            return queryset.none()

        return super().filter_queryset(request, queryset, view)[:10]


class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [RequiredSearchFilter]
    search_fields = ['nickname']


class GlobalStatsView(APIView):

    def get(self, request):
        stats = GlobalStats.objects.all()
        game_filter = request.query_params.get('game', None)
        if game_filter:
            stats = stats.filter(game=game_filter)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
        game_filter = request.query_params.get('game', None)
        player_filter = request.query_params.get('player', None)
        last = request.query_params.get('last', None)
        if not game_filter or not player_filter:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stats = PlayerStats.objects.filter(game=game_filter, player=player_filter).order_by('date')
        if last:
            serializer = PlayerStatsSerializer(stats.last())
        else:
            serializer = PlayerStatsSerializer(stats, many=True)
        return Response(serializer.data)


class PlayerAchievementView(APIView):

    def get(self, request):
        game_filter = request.query_params.get('game', None)
        player_filter = request.query_params.get('player', None)
        if not game_filter or not player_filter:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        achievements = PlayerAchievement.objects.filter(achievement__game=game_filter, player=player_filter)
        serializer = PlayerAchievementSerializer(achievements, many=True)
        return Response(serializer.data)


class AchievementsOverTimeView(APIView):

    def get(self, request):
        game_filter = request.query_params.get('game', None)
        if not game_filter:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        achievements = AchievementsOverTime.objects.filter(game=game_filter).exclude(time=timedelta(0))
        serializer = AchievementsOverTimeSerializer(achievements, many=True)
        return Response(serializer.data)
