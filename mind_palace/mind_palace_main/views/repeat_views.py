from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from mind_palace.mind_palace_main.business_logic.caches.full_metrics_cache import get_cached_full_metrics


class RepeatView(LoginRequiredMixin, TemplateView):
    template_name = 'repeat.jinja.html'

    def get_context_data(self, **kwargs):
        return {
            'url_edit_prefix': f'/{settings.MIND_PALACE_URL_PREFIX}n/',
            'url_edit_postfix': '/edit/',
            'fm': get_cached_full_metrics(self.request.user)
        }
