from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from tralard.models.program import Program
from tralard.models.project import Project
from tralard.models.sub_project import SubProject
from tralard.models.beneficiary import Beneficiary

class ProgramDetailView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = "program"
    template_name = 'project/list.html'

    def get_context_data(self):
        context = super(ProgramDetailView, self).get_context_data()
        context['title'] = 'Projects'
        program_id = self.kwargs['pk']
        program_object = Program.objects.get(id=program_id)
        context['program'] = program_object
        context['total_projects'] = Project.objects.filter(program=program_object).count()
        context['sub_project_list'] = SubProject.objects.all()
        context['beneficiary_list'] = Beneficiary.objects.all()
        context['projects'] = Project.objects.all()
        context['total_sub_projects'] = SubProject.objects.all().count()
        context['total_beneficiary_count'] = Beneficiary.objects.all().count()
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
