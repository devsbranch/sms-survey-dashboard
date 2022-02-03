# -*- coding: utf-8 -*-
from datetime import datetime
import os
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from tralard.models.program import Program
from tralard.models.project import Project
from tralard.forms import (
    ProjectForm,
    Indicator,
    IndicatorTargetForm,
    IndicatorTargetValueForm,
    IndicatorUnitOfMeasureForm,
    IndicatorForm
)
from tralard.models.beneficiary import Beneficiary
from tralard.models.sub_project import Indicator, SubProject


class ProgramDetailView(LoginRequiredMixin, ListView):
    model = Project
    form_class = ProjectForm
    context_object_name = "program"
    template_name = "program/detail.html"

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
            self.projects = Project.objects.filter(
                    program__slug=self.program_object.slug
                ).filter(
                    name__icontains=self.search_query
            )
        else:
            self.projects = Project.objects.filter(
                program__slug=self.program_object.slug
            )

        if self.subproject_search_query:
            self.subprojects = SubProject.objects.filter(
                    project__program__slug=self.program_object.slug
                ).filter(
                    name__icontains=self.subproject_search_query
            )
        else:
            self.subprojects = SubProject.objects.filter(
             project__program__slug=self.program_object.slug
            )

        if self.beneficiary_search_query:
            self.beneficiaries = Beneficiary.objects.filter(
                    sub_project__project__program__slug=self.program_object.slug
                ).filter( 
                    name__icontains=self.beneficiary_search_query
            )
        else:
            self.beneficiaries = Beneficiary.objects.filter(
                sub_project__project__program__slug=self.program_object.slug
            )
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

        indicator_forms = [
            {
                "modal_id": "indicator_form",
                "form": IndicatorForm,
                "modal_header": "Indicator Name",
                "modal_subheader": "Create Indicator Name",
                "action_url": "indicator_name",
            },
            {
                "modal_id": "indicator_target_form",
                "form": IndicatorTargetForm,
                "modal_header": "Indicator Target",
                "modal_subheader": "Create Indicator Target",
                "action_url": "indicator_target",
            },
            {
                "modal_id": "indicator_target_value_form",
                "form": IndicatorTargetValueForm,
                "modal_header": "Indicator Target Value",
                "modal_subheader": "Create Indicator Target Value",
                "action_url": "indicator_target_value",
            },
            {
                "modal_id": "indicator_target_unit_form",
                "form": IndicatorUnitOfMeasureForm,
                "modal_header": "Indicator Unit of Measure",
                "modal_subheader": "Create Indicator Unit of Measure",
                "action_url": "indicator_target_unit",
            },
        ]

        indicators_list = []

        current_year = datetime.now().year

        
        indicators = Indicator.objects.filter(
            subproject_indicators__in=self.subprojects
        ).distinct()

        for indicator in indicators:
            indicator_data = {"name": "", "targets": []}
            indicator_data["name"] = indicator.name
            indicator_data["slug"] = indicator.slug

            targets = indicator.indicatortarget_set.all()
            for target in targets:
                target_dict = {}
                target_dict["id"] = target.id
                target_dict["description"] = target.description
                target_dict["unit_of_measure"] = target.unit_of_measure.unit_of_measure
                target_dict["baseline"] = target.baseline_value
                target_dict["yearly_target_values"] = []
                target_dict["unit_of_measure_id"] = target.unit_of_measure.id

                year_count = 1
                for yearly_target_values in target.indicatortargetvalue_set.all().order_by("year"):
                    yearly_target_values_dict = {}
                    yearly_target_values_dict[f"year_{year_count}"] = {
                        "id": yearly_target_values.id,
                        "year": yearly_target_values.year.year,
                        "target_value": yearly_target_values.target_value,
                        "actual_value": target.unit_of_measure.get_actual_data(
                            indicator
                        ) if yearly_target_values.year.year <= current_year else 0
                    }
                    target_dict["yearly_target_values"].append(
                        yearly_target_values_dict
                    )
                    year_count += 1

                indicator_data["targets"].append(target_dict)
            indicators_list.append(indicator_data)

        context["title"] = "Program Detail"
        context["project_form"] = ProjectForm
        context["projects"] = self.project_paginator_list
        context["program"] = self.program_object
        context["program_slug"] = self.program_slug
        context["sub_project_list"] = self.subproject_paginator_list
        context["sub_project_page_number"] = self.subproject_page_number
        context["beneficiary_list"] = self.beneficiary_paginator_list
        context["total_projects"] = Project.objects.filter(
            program=self.program_object
        ).count()
        context["total_sub_projects"] = SubProject.objects.all().count()
        context["total_beneficiary_count"] = Beneficiary.objects.all().count()
        context["indicators"] = indicators_list
        context["indicator_forms"] = indicator_forms
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.is_ajax():
            project_list_html = render_to_string(
                template_name="includes/project/project-list.html",
                context={"projects": self.projects},
            )
            subprojects_html = render_to_string(
                template_name="includes/sub-project-list.html",
                context={"sub_project_list": self.subprojects},
            )
            beneficiaries_html = render_to_string(
                template_name="includes/beneficiary-list.html",
                context={"beneficiary_list": self.beneficiaries},
            )

            data_dict = {
                "search_result_view": project_list_html,
                "subproj_search_result": subprojects_html,
                "beneficiaries_search_result": beneficiaries_html,
            }
            return JsonResponse(data=data_dict, safe=False)
        else:
            return response


@login_required(login_url="/login/")
def preview_indicator_document(request, program_slug):
    from tralard.tasks import build_indicator_report

    document_directory = f"{settings.MEDIA_ROOT}/temp/reports"

    # for now we just get a recently created file in the directory where the indicator reports are saved
    # we can have a doc that can be generated and updated at regular intervals and ready for preview.
    if not os.path.exists(document_directory):
        os.makedirs(document_directory)

    filenames_list = os.listdir(document_directory)


    # TODO: Add background scheduled task that generates a file ready for preview in the browser

    if not filenames_list:
        # for now this is a temporary work around
        results = build_indicator_report(program_slug)
        filename = results["result"]["filename"]
    else:
        filename = filenames_list[0]

    path = f"temp/reports/{filename}"
    context = {"path": path, "program_slug": program_slug}
    return render(request, "tralard/indicator_report_preview.html", context)
