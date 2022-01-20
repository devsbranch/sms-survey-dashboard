from django.db.models import F
from tralard.models.profile import Profile
from tralard.forms.profile import ProfileForm
from django.db.models import Sum
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
from tralard.models.program import Program
from tralard.models.project import Project
from tralard.models.fund import Fund
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
        self.total_project_funds = Fund.objects.all().aggregate(Sum("amount"))
        self.cleaned_total_project_funds = self.total_project_funds["amount__sum"]
        context["title"] = "Program: Tralard"
        context["program_list"] = Program.objects.all().order_by("-started")[:5]
        context["project_count"] = Project.objects.all().count()
        context["total_project_funds"] = self.cleaned_total_project_funds
        context["subproject_count"] = SubProject.objects.all().count()
        context["beneficiary_count"] = Beneficiary.objects.all().count()
        context["beneficiary_count_male"] = Beneficiary.custom_objects.get_total_males()
        context[
            "beneficiary_count_female"
        ] = Beneficiary.custom_objects.get_total_females()
        context["hhs_count"] = Beneficiary.custom_objects.get_total_hhs()
        context["hhs_count_female"] = Beneficiary.custom_objects.get_female_hhs()
        context["org_type_cooperative"] = (
            Beneficiary.objects.filter(org_type="coorperative").count()
        )
        context["org_type_businessfirm"] = (
            Beneficiary.objects.filter(org_type="businessfirm").count()
        )
        context["org_type_other"] = (
            Beneficiary.objects.filter(org_type="other").count()
        )
        context["total_approved_subprojects"] = (
            SubProject.objects.all().filter(approved=True).count()
        )
        context["total_funded_subprojects"] = (
            SubProject.objects.all().filter(fund=True).count()
        )
        context["total_approved_projects"] = (
            Project.objects.all().filter(approved=True).count()
        )
        context["total_funded_projects"] = (
            Project.objects.all().filter(has_funding=True).count()
        )
        context["prov_labels"] = SubProject.custom_objects.get_sub_projects_district_json()[
            "labels"
        ]
        context["subs_in_prov"] = SubProject.custom_objects.get_sub_projects_district_json()[
            "data"
        ]
        context["projects"] = Project.objects.all()
        context['funds_in_year_label'] = Fund.count_objects.get_total_funds_in_year()['year_labels']
        context['total_funds_in_year'] = Fund.count_objects.get_total_funds_in_year()['total_funds']

        return context


class ProjectListView(LoginRequiredMixin, TemplateView):
    template_name = "tralard/dashboard-crm-deal.html"

    def get_context_data(self):
        context = super(ProjectListView, self).get_context_data()
        context["title"] = "Projects"
        return context

class DashboardExtrasView(LoginRequiredMixin, TemplateView):
    template_name = "tralard/dashboard-chartjs.html"

    def get_context_data(self):
        context = super(DashboardExtrasView, self).get_context_data()
        context["title"] = "Dashboard Extras"
        return context
