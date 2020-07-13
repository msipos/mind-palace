from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from mind_palace.mind_palace_main.business_logic.entities.note_entity import NoteEntity
from mind_palace.mind_palace_main.business_logic.repeat_logic import repeat_note
from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_now
from mind_palace.mind_palace_main.models import Collection
from mind_palace.mind_palace_main.models import Note


class NewNoteAPIView(APIView):
    def post(self, request, **kwargs):
        collection = Collection.get_collection(self.request.user, self.kwargs['id'])
        note = Note(collection=collection, created_time=timestamp_now())
        note_entity = NoteEntity.from_json(request.data)
        note.from_entity(note_entity)
        note.created_time = timestamp_now()
        note.updated_time = timestamp_now()
        note.repeat_time = repeat_note(note_entity.repeat_policy)
        note.save()
        return Response({'note_id': note.id, 'note_url': reverse('view_note', args=[note.id])})
