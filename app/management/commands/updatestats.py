from django.core.management.base import BaseCommand

from app.players_updater import PlayersUpdater
from app.games_updater import GamesUpdater


class Command(BaseCommand):
    help = 'Updates players stats'

    def handle(self, *args, **options):
        updater = PlayersUpdater()
        updater.update_players_stats()
        GamesUpdater.get_average_playtime()
        self.stdout.write(self.style.SUCCESS('Data successfully updated'))
