from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView

from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_to_localtime, timestamp_now
from mind_palace.mind_palace_main.models import Collection, Note
from mind_palace.mind_palace_main.utils import pretty_format_timedelta


class SearchResultsView(LoginRequiredMixin, TemplateView):
    template_name = 'search_results.jinja.html'

    def get_context_data(self, **kwargs):
        collections = Collection.get_collections(self.request.user)
        q_obj = Q(collection__in=collections)

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
            'name', 'created_time', 'updated_time', 'repeat_time', 'collection__id', 'collection__name')
        paginator = Paginator(notes, per_page=12)

        p = int(self.request.GET.get('p', '1'))
        page = paginator.page(p)

        reference_time = timestamp_to_localtime(timestamp_now())

        return {
            'notes': page.object_list,
            'page': page,
            'p': p,
            'q_search': q,
            'paginator': paginator,
            'reference_time': reference_time,
            'pretty_format_timedelta': pretty_format_timedelta
        }