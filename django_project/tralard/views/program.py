
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from tralard.forms.project import ProjectForm
from tralard.models.program import Program
from tralard.models.project import Project
from tralard.models.sub_project import SubProject
from tralard.models.beneficiary import Beneficiary


class ProgramDetailView(LoginRequiredMixin, ListView):
    model = Project
    form_class = ProjectForm
    context_object_name = "program"
    template_name = 'program/detail.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the SubProject list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy('tralard:program-detail', kwargs={
            'program_slug': self.object.program.slug,
            'project_slug': self.object.slug
        })

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(ProgramDetailView, self).get_form_kwargs()
        self.program_slug = self.kwargs.get('program_slug', None)
        self.project_slug = self.kwargs.get('project_slug', None)

        self.program = Program.objects.get(slug=self.program_slug)
        self.project = Project.objects.get(slug=self.project_slug)

        kwargs.update({
            'user': self.request.user,
            'program_slug': self.program,
            'project_slug': self.project
        })

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProgramDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Program Detail'
        context['project_form'] = ProjectForm

        self.program_slug = self.kwargs['program_slug']
        self.program_object = Program.objects.get(slug=self.program_slug)

        context['program'] = self.program_object
        context['total_projects'] = Project.objects.filter(program=self.program_object).count()
        context['sub_project_list'] = SubProject.objects.all()
        context['beneficiary_list'] = Beneficiary.objects.all()
        context['projects'] = Project.objects.filter(program__slug=self.program_object.slug)
        context['total_sub_projects'] = SubProject.objects.all().count()
        context['total_beneficiary_count'] = Beneficiary.objects.all().count()
        return context
