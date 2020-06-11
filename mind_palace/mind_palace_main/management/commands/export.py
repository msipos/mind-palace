import json

from django.core.management.base import BaseCommand

from mind_palace.mind_palace_main.models import Collection, Note


class Command(BaseCommand):
    help = 'Export all the data'

    def handle(self, *args, **options):

        # Dump collections
        collections = Collection.objects.all()
        collections_json = []
        with open('collections.json', 'wt') as f:
            for collection in collections:
                collections_json.append({
                    'id': str(collection.id),
                    'name': collection.name
                })
            json.dump(collections_json, f)

        # Dump notes
        notes = Note.objects.all()
        notes_json = []
        with open('notes.json', 'wt') as f:
            for note in notes:
                note_entity = note.to_entity()
                note_json = note_entity.to_json()
                note_json['collection_id'] = str(note.collection_id)
                notes_json.append(note_json)
            json.dump(notes_json, f)
