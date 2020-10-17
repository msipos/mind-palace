from django.urls import reverse
from rest_framework.response import Response

from mind_palace.mind_palace_main.business_logic.entities.choice_entity import ChoiceEntity
from mind_palace.mind_palace_main.business_logic.learn_logic import create_note_choices
from mind_palace.mind_palace_main.business_logic.repeat_logic import repeat_note
from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_now
from mind_palace.mind_palace_main.models import Collection, Note
from mind_palace.mind_palace_main.views.api_views.base_api_view import BaseAPIView


class RepeatAPIView(BaseAPIView):
    def get(self, request, **kwargs):
        """ This is used for listing. """

        # Get all collections
        collections = Collection.get_collections(self.request.user).only('id')

        # Get all active notes
        active_notes = []
        for collection in collections:
            notes = Note.get_active_notes(collection).only('id', 'repeat_time')
            active_notes.extend(notes)

        if len(active_notes) == 0:
            return Response({
                'num_active_notes': 0
            })

        # Sort active notes by repeat_time
        active_notes.sort(key=lambda x: x.repeat_time)

        # Fetch the top note
        note = Note.objects.get(id=active_notes[0].id)
        note_entity = note.to_entity()

        # Fetch choices
        choices = create_note_choices(note_entity.repeat_policy, note_entity.learn_policy)

        # Get URLs
        url_note_action = reverse("api_note_action", args=[note.id])
        url_list_collection = reverse("list_collection", args=[note.collection.id])
        url_note_edit = reverse("edit_note", args=[note.id])

        return Response({
            'num_active_notes': len(active_notes),
            'active_note': note_entity.to_json(),
            'choices': [
                c.to_json() for c in choices
            ],
            'urls': {
                'url_note_action': url_note_action,
                'url_list_collection': url_list_collection,
                'url_note_edit': url_note_edit
            }
        })

    def post(self, request, **kwargs):
        note_id = request.data['note_id']
        choice = request.data['choice']

        note = Note.get_note_by_id(self.request.user, note_id)
        note_entity = note.to_entity()
        choice_entity = ChoiceEntity.from_json(choice)
        note.last_repeat_time = timestamp_now()
        note.repeat_time = repeat_note(note_entity.repeat_policy, choice_entity)
        if choice_entity.overwrite_repeat_policy:
            assert choice_entity.repeat_policy is not None
            note_entity.repeat_policy = choice_entity.repeat_policy
            note.from_entity(note_entity, load_name=False, load_contents=False, load_metadata=True)
        note.save()
        return Response({})
