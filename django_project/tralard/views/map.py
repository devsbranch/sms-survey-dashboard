from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from tralard.map_utils import build_map_context

class MapTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'tralard/map.html'

    def get_context_data(self):
        context = super(MapTemplateView, self).get_context_data()
        context['title'] = 'Beneficiary Map'
        context['map'] = build_map_context()
        return context

