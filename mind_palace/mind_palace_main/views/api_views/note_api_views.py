from rest_framework.response import Response

from mind_palace.mind_palace_main.business_logic.caches.full_metrics_cache import invalidate_cached_full_metrics
from mind_palace.mind_palace_main.business_logic.entities.note_entity import NoteEntity
from mind_palace.mind_palace_main.business_logic.repeat_logic import repeat_note
from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_now
from mind_palace.mind_palace_main.models import Note
from mind_palace.mind_palace_main.views.api_views.base_api_view import BaseAPIView


class EditNoteAPIView(BaseAPIView):
    def post(self, request, **kwargs):
        invalidate_cached_full_metrics(request.user)

        note = Note.get_note_by_id(self.request.user, self.kwargs['id'])
        note_entity = NoteEntity.from_json(request.data)
        note.from_entity(note_entity)
        note.updated_time = timestamp_now()
        note.repeat_time = repeat_note(note_entity.repeat_policy)
        note.save()
        return Response({})


class NoteActionAPIView(BaseAPIView):
    def post(self, request, **kwargs):
        invalidate_cached_full_metrics(request.user)

        note = Note.get_note_by_id(self.request.user, self.kwargs['id'])
        action = request.data['action']
        if action == 'delete':
            note.delete()
        elif action == 'archive':
            note.archived = True
            note.updated_time = timestamp_now()
            note.save()
        elif action == 'unarchive':
            note.archived = False
            note.updated_time = timestamp_now()
            note.save()
        else:
            raise ValueError(f'Invalid action: {action}')
        return Response({})
