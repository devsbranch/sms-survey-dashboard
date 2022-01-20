from django.http import JsonResponse
from django.urls import reverse_lazy
from django.forms import model_to_dict
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

from tralard.models.program import Program
from tralard.models.project import Project
from tralard.forms.project import ProjectForm
from tralard.models.sub_project import SubProject
from tralard.models.beneficiary import Beneficiary

class ProgramDetailView(LoginRequiredMixin, ListView):
    model = Project
    form_class = ProjectForm
    context_object_name = "program"
    template_name = 'program/detail.html'

    # Used to modify queryset and in context
    search_query = None
    projects = None
    subprojects = None
    beneficiaries = None

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the SubProject list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy(
            "tralard:program-detail",
            kwargs={
                "program_slug": self.object.program.slug,
                "project_slug": self.object.slug,
            },
        )

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(ProgramDetailView, self).get_form_kwargs()
        self.program_slug = self.kwargs.get("program_slug", None)
        self.project_slug = self.kwargs.get("project_slug", None)

        self.program = Program.objects.get(slug=self.program_slug)
        self.project = Project.objects.get(slug=self.project_slug)

        kwargs.update(
            {
                "user": self.request.user,
                "program_slug": self.program,
                "project_slug": self.project,
            }
        )

        return kwargs

    def get_context_data(self):
        context = super(ProgramDetailView, self).get_context_data()
        context["title"] = "Program Detail"

        self.program_slug = self.kwargs["program_slug"]
        self.program_object = Program.objects.get(slug=self.program_slug)
        self.search_query = self.request.GET.get("q")
        self.subproject_search_query = self.request.GET.get("subproject_query")
        self.beneficiary_search_query = self.request.GET.get("beneficiaries_query")

        if self.search_query:
            self.projects = Project.objects.filter(program__slug=self.program_object.slug,
                                                   name__icontains=self.search_query)
        else:
            self.projects = Project.objects.filter(program__slug=self.program_object.slug)

        if self.subproject_search_query:
            self.subprojects = SubProject.objects.filter(name__icontains=self.subproject_search_query)
        else:
            self.subprojects = SubProject.objects.all()

        if self.beneficiary_search_query:
            self.beneficiaries = Beneficiary.objects.filter(name__icontains=self.beneficiary_search_query)
        else:
            self.beneficiaries = Beneficiary.objects.all()
        self.subproject_paginator = Paginator(self.subprojects, 9)
        self.subproject_page_number = self.request.GET.get("subproject_page")
        self.subproject_paginator_list = self.subproject_paginator.get_page(
            self.subproject_page_number
        )
        self.beneficiary_paginator = Paginator(self.beneficiaries, 8)
        self.beneficiary_page_number = self.request.GET.get("beneficiary_page")
        self.beneficiary_paginator_list = self.beneficiary_paginator.get_page(
            self.beneficiary_page_number
        )
        
        self.project_paginator = Paginator(self.projects, 9)
        self.project_page_number = self.request.GET.get("project_page")
        self.project_paginator_list = self.project_paginator.get_page(
            self.project_page_number
        )
        context['title'] = 'Program Detail'
        context['project_form'] = ProjectForm
        context['projects'] = self.project_paginator_list
        context['program'] = self.program_object
        context['sub_project_list'] = self.subproject_paginator_list
        context['sub_project_page_number'] = self.subproject_page_number
        context['beneficiary_list'] = self.beneficiary_paginator_list
        context['total_projects'] = Project.objects.filter(program=self.program_object).count()
        context['total_sub_projects'] = SubProject.objects.all().count()
        context['total_beneficiary_count'] = Beneficiary.objects.all().count()
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.is_ajax():
            project_list_html = render_to_string(
                template_name="includes/project/project-list.html",
                context={"projects": self.projects}
            )
            subprojects_html = render_to_string(
                template_name="includes/sub-project-list.html",
                context={"sub_project_list": self.subprojects}
            )
            beneficiaries_html = render_to_string(
                template_name="includes/beneficiary-list.html",
                context={"beneficiary_list": self.beneficiaries}
            )

            data_dict = {
                "search_result_view": project_list_html,
                "subproj_search_result": subprojects_html,
                "beneficiaries_search_result": beneficiaries_html
            }
            return JsonResponse(data=data_dict, safe=False)
        else:
            return response
