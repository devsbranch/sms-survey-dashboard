from typing import List
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from tralard.models.program import Program
from tralard.models.project import Project, Feedback
from tralard.models.sub_project import SubProject, Indicator
from tralard.models.beneficiary import Beneficiary

from tralard.forms.sub_project import SubProjectForm

class ProjectDetailView(LoginRequiredMixin, ListView):
    model = SubProject
    context_object_name = "project"
    template_name = 'project/detail.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(Project, self).get_form_kwargs()
        self.program_slug = self.kwargs.get('program_slug', None)
        self.project_slug = self.kwargs.get('project_slug', None)

        self.program = Program.objects.get(slug=self.program_slug)
        self.project = Project.objects.get(slug=self.project_slug)

        kwargs.update({
            'user': self.request.user,
            'program': self.program,
            'project': self.project
        })
        
        return kwargs

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the SubProject list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy('tralard:project-detail', kwargs={
            'program_slug': self.object.program.slug,
            'project_slug': self.object.slug
        })

    def get_context_data(self):
        context = super(ProjectDetailView, self).get_context_data()
        context['title'] = 'Project Detail'
        
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)

        self.sub_projects_qs = SubProject.objects.filter(project__slug=self.project_slug)
        self.sub_project_count = self.sub_projects_qs.count()
        self.all_feedback_qs = Feedback.objects.filter(
            project__slug=self.project_slug
            )
        self.all_subproject_indicators = Indicator.objects.filter(
            subproject_indicators__in=self.sub_projects_qs
            )
        context['citizen_feedback_list'] = self.all_feedback_qs
        context['project'] = self.project
        context['indicators'] = self.all_subproject_indicators
        context['form'] = SubProjectForm
        context['sub_project_list'] = self.sub_projects_qs
        context['total_sub_projects'] = self.sub_project_count

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
