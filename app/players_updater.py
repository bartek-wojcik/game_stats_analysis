import string
from datetime import timedelta
from typing import List, Dict
import requests
from django.conf import settings
from app.models import Player, Game, PlayerStats, PlayerAchievement, Achievement
import numpy as np
import logging

logger = logging.getLogger(__name__)

_PLAYER_API = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'
_PLAYER_STATS_API = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={}&key={}&steamid={}'
_PLAYER_GAMES_API = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}'
_PLAYER_ACHIEVEMENTS_API = 'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={}&key={}&steamid={}'


class PlayersUpdater:

    players = Player.objects.all()
    games = Game.objects.all()
    list_ids = players.values_list('id', flat=True)

    def update_players(self):
        PlayersUpdater.update_nicknames_and_avatars(self.list_ids)

    def update_players_stats(self):
        for player in self.players:
            try:
                PlayersUpdater.update_player_stats(player.id)
            except Exception as e:
                logger.error('Error occurred while fetching player stats (ID: {})'.format(player.id), e)

    def update_players_achievements(self):
        for game in self.games:
            game_achievements = list(Achievement.objects.filter(game=game))
            for player in self.players:
                try:
                    PlayersUpdater.__get_player_achievements(player.id, game.id, game_achievements)
                except Exception as e:
                    logger.error('Error occurred while fetching player achievement (Player ID: {} Game ID)'.format(player.id, game.id), e)

    @staticmethod
    def update_nicknames_and_avatars(list_ids: List[str]) -> bool:
        chunks = len(list_ids) // 101 + 1
        for part in np.array_split(list_ids, chunks):
            ids = ','.join(part)
            url = _PLAYER_API.format(settings.STEAM_API_KEY, ids)
            result = requests.get(url)
            data = result.json()
            players = data.get('response', {}).get('players', None)
            if not players:
                continue
            for player in players:
                PlayersUpdater.__update_player(player)
        return True

    @staticmethod
    def __update_player(player: Dict):
        id = player['steamid']
        Player.objects.update_or_create(
            pk=id,
            defaults={
                'nickname': player['personaname'],
                'avatar': player['avatar'],
            }
        )

    @staticmethod
    def update_player_stats(player_id: string):
        url = _PLAYER_GAMES_API.format(settings.STEAM_API_KEY, player_id)
        result = requests.get(url)
        data = result.json()
        playtime_data = data.get('response', {}).get('games', [])
        for playtime in playtime_data:
            PlayersUpdater.__create_player_stats(player_id, playtime['appid'], playtime['playtime_forever'])
        return True

    @staticmethod
    def __create_player_stats(player_id, game_id: int, playtime: int) -> bool:
        if not Game.objects.filter(id=game_id):
            return False
        stats = PlayersUpdater.__get_player_game_stats(player_id, game_id)
        PlayerStats(
            game_id=game_id,
            player_id=player_id,
            time=timedelta(minutes=playtime),
            stats=stats,
        ).save()
        return True

    @staticmethod
    def __get_player_game_stats(player_id: string, game_id: int) -> List[dict]:
        url = _PLAYER_STATS_API.format(game_id, settings.STEAM_API_KEY, player_id)
        result = requests.get(url)
        if not result:
            return []
        data = result.json()
        stats = data.get('playerstats', {}).get('stats', [])
        return stats

    @staticmethod
    def __get_player_achievements(player_id: string, game_id: int, game_achievements: []):
        url = _PLAYER_ACHIEVEMENTS_API.format(game_id, settings.STEAM_API_KEY, player_id)
        result = requests.get(url)
        data = result.json()
        achievement_map = {}
        api_achievements = data('playerstats', {}).get('achievements', [])
        for achievement in api_achievements:
            achievement_map[achievement['apiname']] = achievement['achieved']
        for achievement in game_achievements:
            if achievement.name in achievement_map:
                PlayerAchievement.objects.update_or_create(
                    player_id=player_id,
                    achievement=achievement,
                    defaults={
                        'achieved': achievement_map[achievement.name],
                    }
                )

