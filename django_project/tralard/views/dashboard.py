# -*- coding: utf-8 -*-
from django.db.models import Sum
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from tralard.models.fund import Fund
from tralard.models.profile import Profile
from tralard.models.subcomponent import SubComponent
from tralard.models.project import Project
from tralard.models.sub_project import SubProject
from tralard.models.beneficiary import Beneficiary


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    model = Profile
    template_name = "index.html"

    def get_context_data(self):
        context = super(HomeTemplateView, self).get_context_data()
        try:
            self.current_user_profile = Profile.objects.get(user=self.request.user)
        except:
            self.current_user_profile = None
        self.total_subproject_funds = Fund.objects.all().aggregate(Sum("amount")) # subprojects
        self.cleaned_total_subproject_funds = self.total_subproject_funds["amount__sum"] # subprojects
        self.subcomponents = SubComponent.objects.all()
        self.subcomponent_paginator = Paginator(self.subcomponents, 5)
        self.subcomponent_page_number = self.request.GET.get("subcomponent_page_number", "")
        self.subcomponent_paginator_list = self.subcomponent_paginator.get_page(
            self.subcomponent_page_number
        )

        context["title"] = "Project: Tralard"
        context["project_list"] = Project.objects.all().order_by("-started")[:5]
        context["subcomponent_count"] = SubComponent.objects.all().count()
        context["total_subproject_funds"] = self.cleaned_total_subproject_funds # subproject
        context["subproject_count"] = SubProject.objects.all().count()
        context["beneficiary_count"] = Beneficiary.objects.all().count()
        context["beneficiary_count_male"] = Beneficiary.custom_objects.get_total_males()
        context[
            "beneficiary_count_female"
        ] = Beneficiary.custom_objects.get_total_females()
        context["hhs_count"] = Beneficiary.custom_objects.get_total_hhs()
        context["hhs_count_female"] = Beneficiary.custom_objects.get_female_hhs()
        context["org_type_cooperative"] = Beneficiary.objects.filter(
            org_type="coorperative"
        ).count()
        context["org_type_businessfirm"] = Beneficiary.objects.filter(
            org_type="businessfirm"
        ).count()
        context["org_type_other"] = Beneficiary.objects.filter(org_type="other").count()
        context["total_approved_subprojects"] = (
            SubProject.objects.all().filter(approved=True).count()
        )
        context["total_funded_subprojects"] = (
            SubProject.objects.all().filter(fund=True).count()
        )

        context["total_approved_projects"] = ( # approved 
            SubComponent.objects.all().filter(approved=True).count()
        )
        context["total_funded_projects"] = (
            SubComponent.objects.all().filter(has_funding=True).count()
        )
        context[
            "prov_labels"
        ] = SubProject.custom_objects.get_sub_projects_district_json()["labels"]
        context[
            "subs_in_prov"
        ] = SubProject.custom_objects.get_sub_projects_district_json()["data"]
        context["subcomponents"] = self.subcomponent_paginator_list
        context["funds_in_year_label"] = Fund.count_objects.get_total_funds_in_year()[
            "year_labels"
        ]
        context["total_funds_in_year"] = Fund.count_objects.get_total_funds_in_year()[
            "total_funds"
        ]
        context['subcomponents_in_prov'] = SubProject.custom_objects.get_subcomponents_in_district_json()['data']

        return context


class SubComponentListView(LoginRequiredMixin, TemplateView):
    template_name = "tralard/dashboard-crm-deal.html"

    def get_context_data(self):
        context = super(SubComponentListView, self).get_context_data()
        context["title"] = "SubComponents"
        return context


class DashboardExtrasView(LoginRequiredMixin, TemplateView):
    template_name = "tralard/dashboard-crm-kanban.html"

    def get_context_data(self):
        context = super(DashboardExtrasView, self).get_context_data()
        context["title"] = "Dashboard Extras"
        return context
