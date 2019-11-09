from django.core.management.base import BaseCommand, CommandError

from app.players_updater import PlayersUpdater


class Command(BaseCommand):
    help = 'Updates players stats'

    def handle(self, *args, **options):
        PlayersUpdater.update_all_players()
        self.stdout.write(self.style.SUCCESS('Data successfully updated'))
