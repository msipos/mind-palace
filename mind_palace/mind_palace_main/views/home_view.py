from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from mind_palace.mind_palace_main.business_logic.collection_cache import CollectionCache
from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_now
from mind_palace.mind_palace_main.models import Collection


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.jinja.html'

    def get_context_data(self, **kwargs):
        collections = Collection.get_collections(self.request.user)
        reference_time = timestamp_now()
        caches = [CollectionCache(c, reference_time) for c in collections]
        return {
            'ccs': list(zip(collections, caches))
        }
