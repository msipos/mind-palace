import json

from django.core.management.base import BaseCommand

from mind_palace.mind_palace_main.models import Collection


class Command(BaseCommand):
    help = 'Import collections.json'

    def add_arguments(self, parser):
        parser.add_argument('collection', nargs=1, type=str)

    def handle(self, *args, **options):
        with open(options['collection'][0], 'rt') as f:
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
