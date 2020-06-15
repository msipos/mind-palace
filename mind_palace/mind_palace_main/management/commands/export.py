from django.core.management.base import BaseCommand

from mind_palace.mind_palace_main.business_logic.import_export import export_all_collections, export_all_notes


class Command(BaseCommand):
    help = 'Export all the data'

    def handle(self, *args, **options):
        export_all_collections('collections.json')
        export_all_notes('notes.json')
