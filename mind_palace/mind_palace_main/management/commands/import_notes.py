from django.core.management.base import BaseCommand

from mind_palace.mind_palace_main.business_logic.import_export import import_notes


class Command(BaseCommand):
    help = 'Import notes.json'

    def add_arguments(self, parser):
        parser.add_argument('notes_json', nargs=1, type=str)

    def handle(self, *args, **options):
        import_notes(options['notes_json'][0])
