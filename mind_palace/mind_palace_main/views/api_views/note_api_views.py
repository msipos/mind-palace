from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from mind_palace.mind_palace_main.business_logic.entities.note_entity import NoteEntity
from mind_palace.mind_palace_main.business_logic.repeat_logic import repeat_note
from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_now
from mind_palace.mind_palace_main.models import Note


class EditNoteAPIView(APIView):
    def post(self, request, **kwargs):
        note = Note.get_note_by_id(self.request.user, self.kwargs['id'])
        note_entity = NoteEntity.from_json(request.data)
        note.from_entity(note_entity)
        note.updated_time = timestamp_now()
        note.repeat_time = repeat_note(note_entity.repeat_policy)
        note.save()
        return Response({})


class NoteActionAPIView(APIView):
    def post(self, request, **kwargs):
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


class NoteAttachmentUploadAPIView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format=None):
        file_obj = request.FILES['file']

        print(request.FILES)

        # do some stuff with uploaded file
        return Response(status=204)
