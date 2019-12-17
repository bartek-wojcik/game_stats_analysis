from datetime import date
import requests
from django.conf import settings

from app.models import Achievement, GlobalStats, Game

_ERROR_RESULT = 42
_CURRENT_PLAYERS_API = 'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={}'
_ACHIEVEMENTS_API = 'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={}'
_ACHIEVEMENTS_INFO_API = 'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v0002/?key={}&appid={}'


class GamesUpdater:

    @staticmethod
    def update_all_games():
        games = Game.objects.all()
        for game in games:
            GamesUpdater.update_game(game)
            GamesUpdater.update_achievement_info(game.id)

    @staticmethod
    def update_game(game: Game):
        GamesUpdater.get_global_stats(game)
        GamesUpdater.update_achievements(game.id)

    @staticmethod
    def update_achievement_info(game_id: int):
        url = _ACHIEVEMENTS_INFO_API.format(settings.STEAM_API_KEY, game_id)
        result = requests.get(url)
        data = result.json()
        if not data:
            return
        achievements = data['game'].get('availableGameStats', {}).get('achievements', [])
        for achievement in achievements:
            name = achievement['displayName']
            description = achievement.get('description', None)
            if not description:
                description = name
            Achievement.objects.update_or_create(
                game_id=game_id,
                name=achievement['name'],
                defaults={
                    'icon': achievement['icon'],
                    'display_name': name,
                    'description': description,
                },
            )

    @staticmethod
    def update_achievements(game_id: int):
        url = _ACHIEVEMENTS_API.format(game_id)
        result = requests.get(url)
        data = result.json()
        if not data:
            return False
        achievements = data['achievementpercentages']['achievements']
        for achievement in achievements:
            Achievement.objects.update_or_create(
                game_id=game_id,
                name=achievement['name'],
                defaults={
                    'global_percent': achievement['percent'],
                },
            )
        return True

    @staticmethod
    def get_global_stats(game: Game) -> bool:
        url = _CURRENT_PLAYERS_API.format(game.id)
        result = requests.get(url)
        data = result.json()
        if data['response']['result'] == _ERROR_RESULT:
            return False
        player_count = data['response']['player_count']
        GlobalStats(game_id=game.id, users=player_count).save()
        if player_count > game.max_users:
            game.max_users = player_count
            game.peak_date = date.today()
            game.save()
        return True
