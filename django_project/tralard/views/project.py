from re import template
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ProjectListView(LoginRequiredMixin, TemplateView):
    template_name = 'project/list.html'

    def get_context_data(self):
        context = super(ProjectListView, self).get_context_data()
        context['title'] = 'Projects'
        return context


class SubProjectListView(LoginRequiredMixin, TemplateView):
    template_name = 'project/sub_project_list.html'
    
    def get_context_data(self):
        context = super(SubProjectListView, self).get_context_data()
        context['title'] = 'Sub Project List'
        return context


class SubProjectDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'project/sub_project_detail.html'
    
    def get_context_data(self):
        context = super(SubProjectDetailView, self).get_context_data()
        context['title'] = 'Sub Project Detail'
        return context
