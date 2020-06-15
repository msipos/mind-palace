from django.core.management.base import BaseCommand

from mind_palace.mind_palace_main.business_logic.import_export import import_collections


class Command(BaseCommand):
    help = 'Import collections.json'

    def add_arguments(self, parser):
        parser.add_argument('collection_json', nargs=1, type=str)

    def handle(self, *args, **options):
        import_collections(options['collection_json'][0])
