from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http.response import JsonResponse
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from tralard.models.fund import (
    Disbursement,
    Expenditure,
    Fund,
)
from tralard.models.project import Project
from tralard.forms.fund import FundForm, DisbursementForm
from tralard.utils import user_profile_update_form_validator


class FundListAndCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new Project Fund
    """

    model = Fund
    form_class = FundForm
    template_name = "fund/list.html"

    def get_context_data(self, **kwargs):
        context = super(FundListAndCreateView, self).get_context_data(**kwargs)
        self.program_slug = self.kwargs["program_slug"]
        self.project_slug = self.kwargs["project_slug"]

        self.project = Project.objects.get(slug=self.project_slug)
        self.project_funds_qs = Fund.objects.filter(
            sub_project__project__slug=self.project_slug
        )
        self.user_profile_utils = user_profile_update_form_validator(
            self.request.POST, self.request.user
        )
        context["user_roles"] = self.user_profile_utils[0]
        context["profile"] = self.user_profile_utils[1]
        context["profile_form"] = self.user_profile_utils[2]
        context["project"] = self.project
        context["funds"] = self.project_funds_qs
        context["fund_title"] = "add project fund"
        context["modal_display"] = "none"
        context["form"] = self.form_class
        context["title"] = "funds"
        return context

    def form_valid(self, form):
        form.save()
        return super(FundListAndCreateView, self).form_valid(form)


def fund_detail(request, program_slug, project_slug, fund_slug):
    """
    Display a single fund
    """
    context = {}
    single_fund = Fund.objects.get(slug=fund_slug)
    single_project = Project.objects.get(slug=project_slug)
    disbursements_qs = Disbursement.objects.filter(fund__slug=fund_slug)
    disbursements = []
    for disb in disbursements_qs:
        serialized_disb = {
            "amount": disb.amount.amount,
            "balance": disb.balance.amount,
            "disbursement_date": disb.disbursement_date,
            "currency": disb.currency,
            "fund": disb.fund.slug,
            "total_expenses": disb.get_total_disbursed_expenses,
            "slug": disb.slug,
        }
        disbursements.append(serialized_disb)
    funds = Fund.objects.filter(sub_project__project__slug=single_project.slug).values()
    project = {}
    project["name"] = single_project.name
    project["slug"] = single_project.slug
    project["approved"] = single_project.approved
    project["has_funding"] = single_project.has_funding
    project["description"] = single_project.description
    fund = {}
    fund["amount"] = str(single_fund.amount)
    fund["balance"] = str(single_fund.balance)
    fund["funding_date"] = single_fund.funding_date
    fund["created"] = single_fund.created
    fund["slug"] = single_fund.slug
    context["project"] = project
    context["disbursements"] = disbursements
    context["title"] = "Fund details"
    context["funds"] = funds
    context["form"] = FundForm
    context["modal_display"] = "block"

    return JsonResponse(
        {
            "disbursements": list(disbursements),
            "funds": list(funds),
            "fund": fund,
            "project": project,
        }
    )


class FundDetailView(LoginRequiredMixin, DetailView):
    model = Fund
    context_object_name = "fund"
    template_name = "fund/detail.html"

    def get_context_data(self):
        context = super(FundDetailView, self).get_context_data()
        context["title"] = "Funds"
        return context


@login_required(login_url="/login/")
def fund_delete(request, program_slug, project_slug, fund_slug):
    fund = Fund.objects.get(slug=fund_slug)
    fund.delete()
    messages.success(request, "Fund deleted successfully")
    return redirect(
        reverse_lazy(
            "tralard:fund-list",
            kwargs={"program_slug": program_slug, "project_slug": project_slug},
        )
    )


@login_required
def update_fund(request, program_slug, project_slug, fund_slug):
    form = FundForm()

    fund_obj = Fund.objects.get(slug=fund_slug)

    if fund_obj is not None:
        if request.method == "POST":
            form = FundForm(request.POST, instance=fund_obj)
            if form.is_valid():
                form.save()
                messages.success(request, "Fund updated successfully")
                return redirect(
                    reverse_lazy(
                        "tralard:fund-list",
                        kwargs={
                            "program_slug": program_slug,
                            "project_slug": project_slug,
                        },
                    )
                )
    else:
        messages.error(request, "Fund not found")
        return redirect(
            reverse_lazy(
                "tralard:fund-list",
                kwargs={"program_slug": program_slug, "project_slug": project_slug},
            )
        )
    return redirect(
        reverse_lazy(
            "tralard:fund-list",
            kwargs={"program_slug": program_slug, "project_slug": project_slug},
        )
    )


class DisbursementListAndCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new disbursement
    """

    model = Fund
    form_class = DisbursementForm
    template_name = "fund/list.html"

    def get_context_data(self, **kwargs):
        context = super(DisbursementListAndCreateView, self).get_context_data(**kwargs)
        self.fund_slug = self.kwargs["fund_slug"]
        self.fund = Fund.objects.get(slug=self.fund_slug)
        self.disbursements = Disbursement.objects.filter(fund=self.fund)

        context["fund"] = self.fund


@login_required(login_url="/login/")
def delete_disbursement(
    request, program_slug, project_slug, fund_slug, disbursement_slug
):
    disbursement = Disbursement.objects.get(slug=disbursement_slug)
    if disbursement is None:
        messages.error(request, "Disbursement not found")
        return redirect(
            reverse_lazy(
                "tralard:fund-list",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                    "fund_slug": fund_slug,
                },
            )
        )
    else:
        disbursement.delete()
        messages.success(request, "Disbursement deleted")
        return redirect(
            reverse_lazy(
                "tralard:fund-list",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                    "fund_slug": fund_slug,
                },
            )
        )


@login_required(login_url="/login/")
def update_disbursement(
    request, program_slug, project_slug, fund_slug, disbursement_slug
):
    form = DisbursementForm()

    disbursement_obj = Disbursement.objects.get(slug=disbursement_slug)

    if disbursement_obj is not None:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Disbursement updated successfully")
                return redirect(
                    reverse_lazy(
                        "tralard:fund-list",
                        kwargs={
                            "program_slug": program_slug,
                            "project_slug": project_slug,
                            "fund_slug": fund_slug,
                        },
                    )
                )
    else:
        messages.error(request, "Disbursement not found")
        return redirect(
            reverse_lazy(
                "tralard:fund-list",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                    "fund_slug": fund_slug,
                },
            )
        )


@login_required(login_url="/login/")
def get_disbursement_expenditures(
    request, program_slug, project_slug, fund_slug, disbursement_slug
):
    expenditures_qs = Expenditure.objects.filter(disbursment__slug=disbursement_slug)
    expenditures = []
    for expenditure in expenditures_qs:
        serialized_expenditure = {
            "id": expenditure.id,
            "amount": expenditure.amount.amount,
            "amount_currency": expenditure.amount_currency,
            "created": expenditure.created,
            "currency": expenditure.currency,
            "disbursement_id": expenditure.disbursment.id,
            "expenditure_date": expenditure.expenditure_date,
            "disbursement_slug": expenditure.disbursment.slug,
            "slug": expenditure.slug,
        }
        expenditures.append(serialized_expenditure)
    return JsonResponse({"expenditures": list(expenditures)})
