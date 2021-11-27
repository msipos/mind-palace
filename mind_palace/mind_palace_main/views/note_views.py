import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from mind_palace.mind_palace_main.business_logic.caches.full_metrics_cache import get_cached_full_metrics
from mind_palace.mind_palace_main.models import Note


class ViewNoteView(LoginRequiredMixin, TemplateView):
    template_name = 'view_note.jinja.html'

    def get_context_data(self, **kwargs):
        note = Note.get_note_by_id(self.request.user, self.kwargs['id'])
        note_entity = note.to_entity()
        return {
            'note': note,
            'collection': note.collection,
            'note_json': json.dumps(note_entity.to_json(), indent=4),
            'fm': get_cached_full_metrics(self.request.user)
        }


class EditNoteView(LoginRequiredMixin, TemplateView):
    template_name = 'edit_note.jinja.html'

    def get_context_data(self, **kwargs):
        note = Note.get_note_by_id(self.request.user, self.kwargs['id'])
        note_entity = note.to_entity()
        return {
            'note': note,
            'collection': note.collection,
            'note_json': json.dumps(note_entity.to_json()),
            'fm': get_cached_full_metrics(self.request.user)
        }
