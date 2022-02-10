# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from tralard.models.project import Project
from tralard.models.subcomponent import SubComponent
from tralard.models.beneficiary import Beneficiary
from tralard.models.sub_project import Indicator, SubProject
from tralard.forms.subcomponent import SearchForm, SubComponentForm
from tralard.forms import (
    IndicatorForm,
    IndicatorTargetForm,
    IndicatorTargetValueForm,
    IndicatorUnitOfMeasureForm,
)

class ProjectDetailView(LoginRequiredMixin, ListView):
    model = SubComponent
    form_class = SubComponentForm
    context_object_name = "project"
    template_name = "project/detail.html"

    # Used to modify queryset and in context
    search_query = None
    subcomponents = None
    subprojects = None
    beneficiaries = None

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the SubProject list page for the object's parent SubComponent

        :returns: URL
        rtype: HttpResponse
        """
        return reverse_lazy(
            "tralard:project-detail",
            kwargs={
                "project_slug": self.object.project.slug,
                "subcomponent_slug": self.object.slug,
            },
        )

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(ProjectDetailView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get("project_slug", None)
        self.subcomponent_slug = self.kwargs.get("subcomponent_slug", None)

        self.project = Project.objects.get(slug=self.project_slug)
        self.subcomponent = SubComponent.objects.get(slug=self.subcomponent_slug)

        kwargs.update(
            {
                "user": self.request.user,
                "project_slug": self.project,
                "subcomponent_slug": self.subcomponent,
            }
        )
        return kwargs

    def get_context_data(self):
        context = super(ProjectDetailView, self).get_context_data()
        context["title"] = "Project Detail"

        self.project_slug = self.kwargs["project_slug"]
        self.project_object = Project.objects.get(slug=self.project_slug)
        self.search_query = self.request.GET.get("q")
        self.subproject_search_query = self.request.GET.get("subproject_query")
        self.beneficiary_search_query = self.request.GET.get("beneficiaries_query")

        if self.search_query:
            self.subcomponents = SubComponent.objects.filter(
                project__slug=self.project_object.slug
            ).filter(name__icontains=self.search_query)
        else:
            self.subcomponents = SubComponent.objects.filter(
                project__slug=self.project_object.slug
            )

        if self.subproject_search_query:
            self.subprojects = SubProject.objects.filter(
                subcomponent__project__slug=self.project_object.slug
            ).filter(name__icontains=self.subproject_search_query)
        else:
            self.subprojects = SubProject.objects.filter(
                subcomponent__project__slug=self.project_object.slug
            )

        if self.beneficiary_search_query:
            self.beneficiaries = Beneficiary.objects.filter(
                sub_project__subcomponent__project__slug=self.project_object.slug
            ).filter(name__icontains=self.beneficiary_search_query)
        else:
            self.beneficiaries = Beneficiary.objects.filter(
                sub_project__subcomponent__project__slug=self.project_object.slug
            )
        self.total_subproject_count = SubProject.objects.all().count()
        self.total_beneficiary_count = Beneficiary.objects.all().count()
        self.total_subcomponent_count = SubComponent.objects.filter(
            project=self.project_object
        ).count()
        
        try:
            self.subcomponent_list = []
            self.subproject_list = []
            self.beneficiary_list = []
            self.district_id = int(self.request.GET.get("district"))
            self.ward_id = int(self.request.GET.get("ward"))
            
            self.sub_projects = SubProject.objects.filter(
                subcomponent__project__slug=self.project_slug,
                ward__district__id=self.district_id,
            )
            
            for sub_project in self.sub_projects:
                self.subcomponent_list.append(
                    sub_project.subcomponent
                )
                self.beneficiary  = Beneficiary.objects.filter(
                    sub_project__subcomponent__project__slug=self.project_slug,
                    ward__district__id=sub_project.ward.district.id,
                )
                self.beneficiary_list.append(
                    self.beneficiary
                )
            self.subcomponents = self.subcomponent_list
            self.total_subcomponent_count = len(self.subcomponent_list)
            
            self.subprojects = self.sub_projects
            self.total_subproject_count = self.subprojects.count()
            
            self.beneficiaries = self.beneficiary_list
            self.total_beneficiary_count = len(self.beneficiary_list)
        except:
            pass
        
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
        self.subcomponent_paginator = Paginator(self.subcomponents, 9)
        self.subcomponent_page_number = self.request.GET.get("subcomponent_page")
        self.subcomponent_paginator_list = self.subcomponent_paginator.get_page(
            self.subcomponent_page_number
        )

        self.subproject_indicator_list = SubProject.objects.filter(
             subcomponent__project__slug=self.project_object.slug
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
             indicator_related_subprojects__in=self.subproject_indicator_list
        ).distinct()
            
        for indicator in indicators:
            indicator_data = {
                "name": indicator.name,
                "targets": [],
                "slug": indicator.slug,
            }
            targets = indicator.indicatortarget_set.all()
            for target in targets:
                target_dict = {
                    "id": target.id,
                    "description": target.description,
                    "unit_of_measure": target.unit_of_measure.unit_of_measure,
                    "baseline": target.baseline_value,
                    "yearly_target_values": [],
                    "unit_of_measure_id": target.unit_of_measure.id,
                }
                target_values = target.indicatortargetvalue_set.all().order_by("year")
                for year_count, yearly_target_values in enumerate(
                    target_values, start=1
                ):
                    yearly_target_values_dict = {
                        f"year_{year_count}": {
                            "id": yearly_target_values.id,
                            "year": yearly_target_values.year.year,
                            "target_value": yearly_target_values.target_value,
                            "actual_value": target.unit_of_measure.get_actual_data(
                                indicator
                            )
                            if yearly_target_values.year.year <= current_year
                            else 0,
                        }
                    }
                    target_dict["yearly_target_values"].append(
                        yearly_target_values_dict
                    )
                indicator_data["targets"].append(target_dict)
            indicators_list.append(indicator_data)

        context["title"] = "Project Detail"
        context["subcomponent_form"] = SubComponentForm
        context["search_form"] = SearchForm
        context["subcomponents"] = self.subcomponent_paginator_list
        context["project"] = self.project_object
        context["project_slug"] = self.project_slug
        context["sub_project_list"] = self.subproject_paginator_list
        context["sub_project_page_number"] = self.subproject_page_number
        context["beneficiary_list"] = self.beneficiary_paginator_list
        context["total_subcomponents"] = self.total_subcomponent_count
        context["total_sub_projects"] = self.total_subproject_count
        context["total_beneficiary_count"] = self.total_beneficiary_count
        context["indicators"] = indicators_list
        context["indicator_forms"] = indicator_forms
        return context


    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.is_ajax():
            subcomponent_list_html = render_to_string(
                template_name="includes/subcomponent/subcomponent-list.html",
                context={"subcomponents": self.subcomponents},
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
                "search_result_view": subcomponent_list_html,
                "subproj_search_result": subprojects_html,
                "beneficiaries_search_result": beneficiaries_html,
            }
            return JsonResponse(data=data_dict, safe=False)
        else:
            return response


@login_required(login_url="/login/")
def preview_indicator_document(request, project_slug):
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
        results = build_indicator_report(project_slug)
        filename = results["result"]["filename"]
    else:
        filename = filenames_list[0]

    path = f"temp/reports/{filename}"
    context = {"path": path, "project_slug": project_slug}
    return render(request, "tralard/indicator_report_preview.html", context)
