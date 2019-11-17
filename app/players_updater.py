import string
from datetime import timedelta
from typing import List, Dict
import requests
from django.conf import settings
from app.models import Player, Game, PlayerStats
import numpy as np

_PLAYER_API = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'
_PLAYER_STATS_API = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={}&key={}&steamid={}'
_PLAYER_GAMES_API = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}'
_PLAYER_ACHIEVEMENTS_API = 'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={}&key={}&steamid={}'


class PlayersUpdater:

    @staticmethod
    def update_all_players():
        players = Player.objects.all()
        list_ids = players.values_list('id', flat=True)
        PlayersUpdater.update_nicknames_and_avatars(list_ids)
        for player in players:
            PlayersUpdater.update_player_stats(player.id)

    @staticmethod
    def update_nicknames_and_avatars(list_ids: List[str]) -> bool:
        chunks = len(list_ids) // 101 + 1
        for part in np.array_split(list_ids, chunks):
            ids = ','.join(part)
            url = _PLAYER_API.format(settings.STEAM_API_KEY, ids)
            result = requests.get(url)
            data = result.json()
            players = data['response']['players']
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
        if not data['response']:
            return {}
        playtime_data = data['response']['games']
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
        stats = data['playerstats']['stats']
        return stats
