from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'tralard/index.html'

    def get_context_data(self):
        context = super(HomeTemplateView, self).get_context_data()
        context['title'] = 'Program: Tralard'
        return context

class ProjectListView(LoginRequiredMixin, TemplateView):
    template_name = 'tralard/dashboard-crm-deal.html'

    def get_context_data(self):
        context = super(ProjectListView, self).get_context_data()
        context['title'] = 'Projects'
        return context


