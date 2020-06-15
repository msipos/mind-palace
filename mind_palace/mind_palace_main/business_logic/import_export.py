import json

from mind_palace.mind_palace_main.business_logic.entities.note_entity import NoteEntity
from mind_palace.mind_palace_main.models import Collection, Note


def export_all_collections(filename: str):
    collections = Collection.objects.all()
    collections_json = []
    with open(filename, 'wt') as f:
        for collection in collections:
            collections_json.append({
                'id': str(collection.id),
                'name': collection.name
            })
        json.dump(collections_json, f)


def export_all_notes(filename: str):
    notes = Note.objects.all()
    notes_json = []
    with open(filename, 'wt') as f:
        for note in notes:
            note_entity = note.to_entity()
            note_json = note_entity.to_json()
            note_json['collection_id'] = str(note.collection_id)
            notes_json.append(note_json)
        json.dump(notes_json, f)


def import_notes(filename: str):
    with open(filename, 'rt') as f:
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


def import_collections(filename: str):
    with open(filename, 'rt') as f:
        collections_json = json.load(f)
        for collection_json in collections_json:
            try:
                collection = Collection.objects.get(id=collection_json['id'])
                print(f'Found existing collection: {collection.id}')
            except:
                collection = Collection(id=collection_json['id'])
                print(f'New collection: {collection.id}')
            collection.name = collection_json['name']
            print(f'... name={collection_json["name"]}')
            collection.save()
