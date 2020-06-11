import json

from django.core.management.base import BaseCommand

from mind_palace.mind_palace_main.business_logic.entities.note_entity import NoteEntity
from mind_palace.mind_palace_main.models import Collection, Note


class Command(BaseCommand):
    help = 'Import notes.json'

    def add_arguments(self, parser):
        parser.add_argument('notes', nargs=1, type=str)

    def handle(self, *args, **options):
        with open(options['notes'][0], 'rt') as f:
            notes_json = json.load(f)
            for note_json in notes_json:
                try:
                    note = Note.objects.get(id=note_json['note_id'])
                    print(f'Found existing note: {note.id}')
                except:
                    note = Note(id=note_json['note_id'])
                    print(f'New note: {note.id}')
                # Get collection
                collection = Collection.objects.get(id=note_json['collection_id'])
                note.collection = collection
                note_entity = NoteEntity.from_json(note_json)
                note.from_entity(note_entity)

                note.created_time = note_entity.created_time
                note.updated_time = note_entity.updated_time
                note.repeat_time = note_entity.repeat_time
                print(f'... name: {note.name}')
                note.save()
