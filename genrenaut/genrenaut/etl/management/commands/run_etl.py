from django.core.management.base import BaseCommand
from etl.etl_process import run_etl_process, update_genre_descriptions

class Command(BaseCommand):
    help = 'Run the ETL process to update genres and songs'

    def handle(self, *args, **options):
        run_etl_process()
        update_genre_descriptions()
        self.stdout.write(self.style.SUCCESS('ETL process completed successfully'))