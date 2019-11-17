from django.core.management.base import BaseCommand, CommandError

from app.players_updater import PlayersUpdater


class Command(BaseCommand):
    help = 'Updates players stats'

    def handle(self, *args, **options):
        updater = PlayersUpdater()
        updater.update_players_stats()
        self.stdout.write(self.style.SUCCESS('Data successfully updated'))
