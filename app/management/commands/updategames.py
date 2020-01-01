from django.core.management.base import BaseCommand

from app.games_updater import GamesUpdater


class Command(BaseCommand):
    help = 'Updates games stats'

    def handle(self, *args, **options):
        GamesUpdater.update_all_games()
        self.stdout.write(self.style.SUCCESS('Data successfully updated'))
