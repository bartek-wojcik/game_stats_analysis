from django.core.management.base import BaseCommand

from app.players_updater import PlayersUpdater


class Command(BaseCommand):
    help = 'Updates players data'

    def handle(self, *args, **options):
        updater = PlayersUpdater()
        updater.update_players()
        self.stdout.write(self.style.SUCCESS('Data successfully updated'))
