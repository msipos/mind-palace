from django.db.models import Q

from mind_palace.mind_palace_main.models import Collection, Note


class CollectionCache:
    def __init__(self, collection: Collection, reference_time: int):
        self.collection = collection

        self.num_total = Note.objects.filter(collection=collection).count()
        self.num_archived = Note.objects.filter(
            Q(collection=collection) & Q(archived=True)
        ).count()
        self.num_active = Note.get_active_notes(collection, reference_time).count()
