import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView

from mind_palace.mind_palace_main.business_logic.entities.contents_entity import ContentsEntity
from mind_palace.mind_palace_main.business_logic.entities.learn_policy_entity import LearnPolicyEntity, LearnPolicyType
from mind_palace.mind_palace_main.business_logic.entities.note_entity import NoteEntity
from mind_palace.mind_palace_main.business_logic.entities.repeat_policy_entity import RepeatPolicyEntity, RepeatPolicyType, TimeOfDay
from mind_palace.mind_palace_main.business_logic.entities.section_entity import MarkdownSectionEntity
from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_to_localtime, timestamp_now, localtime_now
from mind_palace.mind_palace_main.models import Collection, Note
from mind_palace.mind_palace_main.utils import pretty_format_timedelta


class ListCollectionView(LoginRequiredMixin, TemplateView):
    template_name = 'list_collection.jinja.html'

    def get_context_data(self, **kwargs):
        collection = Collection.get_collection(self.request.user, self.kwargs['id'])
        q_obj = Q(collection=collection)

        q = self.request.GET.get('q', '').strip()
        filter_for_archived = False
        if q:
            for word in q.split():
                if word.lower() == 'archived':
                    filter_for_archived = True
                else:
                    q_obj = q_obj & Q(name__icontains=word)

        if filter_for_archived:
            q_obj = q_obj & Q(archived=True)
        else:
            q_obj = q_obj & Q(archived=False)
        notes = Note.objects.filter(q_obj).order_by('-updated_time').only(
            'name', 'created_time', 'updated_time', 'repeat_time')
        paginator = Paginator(notes, per_page=12)

        p = int(self.request.GET.get('p', '1'))
        page = paginator.page(p)

        reference_time = timestamp_to_localtime(timestamp_now())

        return {
            'notes': page.object_list,
            'page': page,
            'p': p,
            'q': q,
            'paginator': paginator,
            'collection': collection,
            'reference_time': reference_time,
            'pretty_format_timedelta': pretty_format_timedelta
        }


class NewNoteView(LoginRequiredMixin, TemplateView):
    template_name = 'new_note.jinja.html'

    def get_context_data(self, **kwargs):
        # Is it a diary?
        is_diary = ('diary' in self.request.GET)

        # Get collection
        collection = Collection.get_collection(self.request.user, self.kwargs['id'])

        # Handle name
        name = ''
        if is_diary:
            dt_now = localtime_now()
            name = dt_now.strftime('Diary, %A, %Y-%m-%d')

        # TODO: Configurable default repeat and learn policies
        repeat_policy = RepeatPolicyEntity(RepeatPolicyType.DAILY, days=1, time_of_day=TimeOfDay.MORNING)
        if is_diary:
            repeat_policy = RepeatPolicyEntity(RepeatPolicyType.DAILY, days=365, time_of_day=TimeOfDay.MORNING)
        learn_policy = LearnPolicyEntity(LearnPolicyType.EXPONENTIAL)

        note_entity = NoteEntity(name, ContentsEntity([MarkdownSectionEntity("")]), repeat_policy=repeat_policy,
                                 learn_policy=learn_policy)
        return {
            'note_json': json.dumps(note_entity.to_json()),
            'collection': collection
        }
