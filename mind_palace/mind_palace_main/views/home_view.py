from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.views import View
from django.views.generic import TemplateView

from mind_palace.mind_palace_main.business_logic.caches.full_metrics_cache import get_cached_full_metrics


class RootView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound('not found')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.jinja.html'

    def get_context_data(self, **kwargs):
        full_metrics = get_cached_full_metrics(self.request.user)
        return {
            'fm': full_metrics
        }
