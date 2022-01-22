# -*- coding: utf-8 -*-
__author__ = "Alison Mukoma <mukomalison@gmail.com>"
__date__ = "31/12/2021"
__revision__ = "$Format:%H$"
__copyright__ = "sonlinux bei DigiProphets 2021"
__annotations__ = "Written from 31/12/2021 23:34 AM CET -> 01/01/2022, 00:015 AM CET"

"""
View classes for a SubProject
"""

# noinspection PyUnresolvedReferences
import logging

from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.urls import reverse_lazy
from braces.views import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    JsonResponse,
    HttpResponseRedirect,
    Http404
)
from django.shortcuts import (
    get_object_or_404,
    redirect
)
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)

from tralard.models.training import Training
from tralard.forms.training import TrainingForm
from tralard.forms import BeneficiaryCreateForm
from tralard.models.fund import Disbursement, Fund
from tralard.forms.sub_project import SubProjectForm
from tralard.models import (
    Beneficiary,
    Project,
    SubProject
)
from tralard.forms.fund import (
    ExpenditureForm,
    FundForm,
    DisbursementForm
)

logger = logging.getLogger(__name__)


class JSONResponseMixin(object):
    """A mixin that can be used to render a JSON response."""

    def render_to_json_response(self, context, **response_kwargs):
        """Returns a JSON response, transforming 'context' to make the payload.

        :param context: Context data to use with template
        :type context: dict

        :param response_kwargs: Keyword args
        :type response_kwargs: dict

        :returns A HttpResponse object that contains JSON
        :rtype: HttpResponse
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type="application/json",
            **response_kwargs,
        )

    @staticmethod
    def convert_context_to_json(context):
        """Convert the context dictionary into a JSON object

        :param context: Context data to use with template
        :type context: dict

        :return: JSON representation of the context
        :rtype: str
        """
        result = "{\n"
        first_flag = True
        for sub_project in context["sub_projects"]:
            if not first_flag:
                result += ",\n"
            result += '    "%s" : "%s"' % (sub_project.slug, sub_project.name)
            first_flag = False
        result += "\n}"
        return result


class SubProjectMixin(object):
    """Mixin class to provide standard settings for a SubProject."""

    model = SubProject  # implies -> queryset = SubProject.objects.all()
    form_class = SubProjectForm


class JSONSubProjectListView(SubProjectMixin, JSONResponseMixin, ListView):
    """List view for a SubProject as json object - needed by javascript."""

    context_object_name = "sub_projects"

    def dispatch(self, request, *args, **kwargs):
        """Ensure this view is only used via ajax.

        :param request: Http request - passed to base class.
        :type request: HttpRequest, WSGIRequest

        :param args: Positional args - passed to base class.
        :type args: tuple

        :param kwargs: Keyword args - passed to base class.
        :type kwargs: dict
        """
        if not request.is_ajax():
            raise Http404("This is an ajax view, friend.")
        return super(JSONSubProjectListView, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """Render this version as markdown [just in case we need this format serialization].

        :param context: Context data to use with template.
        :type context: dict

        :param response_kwargs: A dict of arguments to pass to the renderer.
        :type response_kwargs: dict

        :returns: A rendered template with mime type application/text.
        :rtype: HttpResponse
        """
        return self.render_to_json_response(context, **response_kwargs)

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which to show all versions of project.
        :rtype: QuerySet
        :raises: Http404
        """
        project_slug = self.kwargs["project_slug"]
        project = get_object_or_404(Project, slug=project_slug)
        qs = SubProject.objects.all().filter(project=project)
        return qs


class SubProjectTrainingListView(LoginRequiredMixin, CreateView):
    model = Training
    form_class = TrainingForm
    template_name = "project/sub-project-training-list.html"

    def get_success_url(self):
        return reverse_lazy(
            "tralard:subproject-training",
            kwargs={
                "program_slug": self.kwargs.get("program_slug", None),
                "project_slug": self.kwargs.get("project_slug", None),
                "subproject_slug": self.kwargs.get("subproject_slug", None),
            },
        )

    def get_context_data(self):
        context = super(SubProjectTrainingListView, self).get_context_data()
        self.subproject_slug = self.kwargs.get("subproject_slug", None)
        self.sub_project_trainings = (
            Training.objects.all().filter(sub_project__slug=self.subproject_slug).all()
        )
        context["title"] = "Sub Project Trainings"
        context["program_slug"] = self.kwargs.get("program_slug", None)
        context["project_slug"] = self.kwargs.get("project_slug", None)
        context["subproject_slug"] = self.kwargs.get("subproject_slug", None)
        context["total_beneficiaries"] = Beneficiary.objects.all().count()
        
        self.training_paginator = Paginator(self.sub_project_trainings, 10)
        self.training_page_number = self.request.GET.get("training_page")
        self.training_paginator_list = self.training_paginator.get_page(self.training_page_number)
        context["trainings"] = self.training_paginator_list
        return context


class SubProjectTrainingUpdateView(LoginRequiredMixin, UpdateView):
    model = Training
    form_class = TrainingForm
    template_name = "includes/sub-project-training-update-modal.html"

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            program_slug = self.kwargs.get("program_slug", None)
            project_slug = self.kwargs.get("project_slug", None)
            subproject_slug = self.kwargs.get("subproject_slug", None)

            return redirect(
                reverse_lazy(
                    "tralard:subproject-training",
                    kwargs={
                        "program_slug": program_slug,
                        "project_slug": project_slug,
                        "subproject_slug": subproject_slug,
                    },
                )
            )

class SubProjectTrainingUpdateView(LoginRequiredMixin, UpdateView):
    model = Training
    form_class = TrainingForm
    template_name = "includes/sub-project-training-update-modal.html"

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            program_slug = self.kwargs.get("program_slug", None)
            project_slug = self.kwargs.get("project_slug", None)
            subproject_slug = self.kwargs.get("subproject_slug", None)

            return redirect(
                reverse_lazy(
                    "tralard:subproject-training",
                    kwargs={
                        "program_slug": program_slug,
                        "project_slug": project_slug,
                        "subproject_slug": subproject_slug,
                    },
                )
            )
            
            
@login_required(login_url="/login/")
def sub_project_training_update(
        request, program_slug, project_slug, subproject_slug, training_entry_slug
):
    form = TrainingForm()
    training = Training.objects.get(slug=training_entry_slug)
    if request.method == "POST":
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect(
                reverse_lazy(
                    "tralard:subproject-training",
                    kwargs={
                        "program_slug": program_slug,
                        "project_slug": project_slug,
                        "subproject_slug": subproject_slug,
                    },
                )
            )
        return redirect(
            reverse_lazy(
                "tralard:subproject-training",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                },
            )
        )


@login_required(login_url="/login/")
def sub_project_update(
        request, program_slug, subproject_slug
):
    subproject = SubProject.objects.get(slug=subproject_slug)
    if request.method == "POST":
        form = SubProjectForm(request.POST or None, request.FILES, instance=subproject)
        if form.is_valid():
            custom_description = form.cleaned_data["custom_description"]
            custom_focus_area = form.cleaned_data["custom_focus_area"]
            form.save()
            
            if custom_description:
                subproject.description = custom_description
            if custom_focus_area:
                subproject.focus_area = custom_focus_area
            subproject.save()
        
        messages.add_message(request, messages.SUCCESS, "SubProject updated successfully!")
        return redirect(
            reverse_lazy(
                "tralard:program-detail",
                kwargs={
                    "program_slug": program_slug,
                },
            )
        )
        

@login_required(login_url="/login/")
def sub_project_training_delete(
        request, program_slug, project_slug, subproject_slug, training_entry_slug
):
    training = Training.objects.get(slug=training_entry_slug)
    training.delete()
    return redirect(
        reverse_lazy(
            "tralard:subproject-training",
            kwargs={
                "program_slug": program_slug,
                "project_slug": project_slug,
                "subproject_slug": subproject_slug,
            },
        )
    )
    

class SubProjectListView(LoginRequiredMixin, SubProjectMixin, ListView):
    """Listed view for SubProject."""

    model = SubProject
    context_object_name = "sub_projects"
    template_name = "tralard/sub_project/list.html"

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SubProjectListView, self).get_context_data(**kwargs)
        context["num_sub_projects"] = context["sub_projects"].count()
        project_slug = self.kwargs.get("project_slug", None)
        context["form"] = SubProjectForm
        context["project_slug"] = project_slug
        if project_slug:
            context["the_project"] = Project.objects.get(slug=project_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :returns: A queryset to show all SubProject.

        :param queryset: Optional queryset.
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            project_slug = self.kwargs.get("project_slug", None)
            if project_slug:
                try:
                    project = Project.objects.get(slug=project_slug)
                except Project.DoesNotExist:
                    raise Http404(
                        "Sorry! The project you are requesting a subproject for "
                        "could not be found or you do not have permission to "
                        "view the subproject. Try logging in as a staff member "
                        "if you wish to view it."
                    )
                queryset = (
                    SubProject.objects.all().filter(project=project).order_by("name")
                )
                return queryset
            else:
                raise Http404(
                    "Sorry! We could not find the project for your subproject!"
                )
        else:
            return queryset


class SubProjectDetailView(SubProjectMixin, DetailView):
    """Detail view for SubProject."""

    context_object_name = "sub_project"
    template_name = "project/sub_project_detail.html"

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because SubProject ids are unique within a Project, we need to make
        sure that we fetch the correct SubProject from the correct Project

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a project
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            queryset = self.get_queryset()
        project_slug = self.kwargs.get("project_slug", None)
        sub_project_slug = self.kwargs.get("subproject_slug", None)
        if project_slug:
            try:
                project = Project.objects.get(slug=project_slug)
            except Project.DoesNotExist:
                raise Http404(
                    "The project you requested a subcateogrty for does not exist."
                )
            try:
                obj = queryset.get(project=project, slug=sub_project_slug)
                return obj
            except SubProject.DoesNotExist:
                raise Http404("The subproject you requested does not exist.")
        else:
            raise Http404("Sorry! We could not find your subproject!")

    def get_context_data(self, **kwargs):
        sub_project = self.get_object()
        sub_proj_indicators = sub_project.indicators.all()
        indicators = []

        for indicator_object in sub_proj_indicators:
            indicator_data = {}
            indicator_data["name"] = indicator_object.name
            indicator_data["indicator_targets"] = indicator_object.indicatortarget_set.all().order_by("start_date")
            indicators.append(indicator_data)

        context = super(SubProjectDetailView, self).get_context_data(**kwargs)
        context["title"] = "Sub Project"
        context["indicators"] = indicators
        return context


# noinspection PyAttributeOutsideInit
class SubProjectDeleteView(LoginRequiredMixin, SubProjectMixin, DeleteView):
    """Delete view for a SubProject."""

    context_object_name = "sub_project"
    template_name = "tralard/sub_project_delete.html"

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.project_slug = self.kwargs.get("project_slug", None)
        self.project = Project.objects.get(slug=self.project_slug)
        return super(SubProjectDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.project_slug = self.kwargs.get("project_slug", None)
        self.project = Project.objects.get(slug=self.project_slug)
        return super(SubProjectDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the SubProject list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy(
            "subproject-list", kwargs={"project_slug": self.object.project.slug}
        )

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the SubProject objects by Project before passing to
        get_object() to ensure that we return the correct SubProject object.
        The requesting User must be authenticated

        :returns: SubProject queryset filtered by Project
        :rtype: QuerySet
        :raises: Http404
        """
        if not self.request.user.is_authenticated:
            raise Http404
        qs = SubProject.objects.filter(project=self.project)
        return qs


# noinspection PyAttributeOutsideInit
class SubProjectCreateView(LoginRequiredMixin, SubProjectMixin, CreateView):
    """Create view for SubProject."""

    context_object_name = "sub_project"
    template_name = "tralard/sub-project-create.html"

    def get_success_url(self):
        """Define the redirect URL

         After successful creation of the object, the User will be redirected
         to the unapproved SubProject list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy(
            "tralard:subproject-list", kwargs={"project_slug": self.object.project.slug}
        )

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SubProjectCreateView, self).get_context_data(**kwargs)
        context["categories"] = self.get_queryset().filter(project=self.project)
        return context

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving.

        :param form: form to validate
        :type form: SubProjectForm

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect
        """
        try:
            super(SubProjectCreateView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError("ERROR: SubProject by this name already exists!")

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SubProjectCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get("project_slug", None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({"project": self.project})
        return kwargs


# noinspection PyAttributeOutsideInit
class SubProjectUpdateView(LoginRequiredMixin, SubProjectMixin, UpdateView):
    """Update view for SubProject."""

    context_object_name = "sub_project"
    template_name = "tralard/sub-project-update.html"

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SubProjectUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get("project_slug", None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({"project": self.project})
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SubProjectUpdateView, self).get_context_data(**kwargs)
        context["categories"] = self.get_queryset().filter(project=self.project)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to show all projects which
        user created (staff gets all projects)
        :rtype: QuerySet
        """
        project_slug = self.kwargs.get("project_slug", None)
        project = Project.objects.get(slug=project_slug)
        qs = SubProject.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(
                Q(project=project)
                & (
                        Q(project__project_funders=self.request.user)
                        | Q(project__project_managers=self.request.user)
                        | Q(project__project_representatives=self.request.user)
                )
            )

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected
        to the SubProject list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy(
            "tralard:subproject-list", kwargs={"project_slug": self.object.project.slug}
        )

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(SubProjectUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError("ERROR: SubProject by this name already exists!")


class PaginatorMixin(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


class SubProjectBeneficiaryOrgListView(
    LoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Beneficiary
    template_name = "beneficiary/list.html"
    form_class = BeneficiaryCreateForm
    paginate_by = 20
    paginator_class = PaginatorMixin

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "tralard:subproject-manage",
            kwargs={
                "program_slug": self.kwargs.get("program_slug", None),
                "project_slug": self.kwargs.get("project_slug", None),
                "sub_project": self.kwargs.get("sub_project", None),
            },
        )

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return response

    def get_context_data(self, **kwargs):
        context = super(SubProjectBeneficiaryOrgListView, self).get_context_data(
            **kwargs
        )

        subproject_slug = self.kwargs.get("subproject_slug", None)
        project_slug = self.kwargs.get("project_slug", None)
        beneficiary_objects = Beneficiary.objects.filter(
            sub_project__slug=subproject_slug
        )
        project = Project.objects.get(slug=project_slug)

        # Just get the sub project name from one beneficiary since we are filtering
        # by a sub project.
        try:
            sub_header = f"Showing all Beneficiaries under the <b>{beneficiary_objects[0].sub_project.name}</b> Sub Project."
        except IndexError:
            sub_header = "There are currently no Beneficiaries under this Sub-Project."

        page = self.request.GET.get("page", 1)
        paginator = self.paginator_class(beneficiary_objects, self.paginate_by)
        organizations = paginator.page(page)
        context["header"] = "Beneficiaries"
        context["project"] = project
        context["beneficiaries"] = organizations
        context["sub_header"] = sub_header
        return context


class SubProjectFundListAndCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new Sub Project Fund
    """

    model = Fund
    form_class = FundForm
    disbursement_form_class = DisbursementForm
    expenditure_form_class = ExpenditureForm
    template_name = "project/fund-list.html"

    def get_success_url(self):
        """
        After successful creation of the object, the User will be redirected
        to the SubProject list page for the object's parent Project
        """
        return reverse_lazy(
            "tralard:subproject-fund-list",
            kwargs={
                "program_slug": self.object.sub_project.project.program.slug,
                "project_slug": self.object.sub_project.project.slug,
                "subproject_slug": self.object.sub_project.slug,
            },
        )

    def get_context_data(self, **kwargs):
        context = super(SubProjectFundListAndCreateView, self).get_context_data(
            **kwargs
        )
        self.program_slug = self.kwargs["program_slug"]
        self.subproject_slug = self.kwargs["subproject_slug"]

        self.sub_project = SubProject.objects.get(slug=self.subproject_slug)
        self.subproject_funds_qs = Fund.objects.filter(
            sub_project__slug=self.subproject_slug
        )
        context["sub_project"] = self.sub_project
        context["funds"] = self.subproject_funds_qs
        context["fund_title"] = "add sub project fund"
        context["modal_display"] = "none"
        context["form"] = self.form_class
        context["disbursement_form"] = self.disbursement_form_class
        context["expenditure_form"] = self.expenditure_form_class
        context["disbursement_title"] = "create fund disbursement"
        context["title"] = "funds"
        return context

    def form_valid(self, form):
        form.save()
        return super(SubProjectFundListAndCreateView, self).form_valid(form)


def subproject_fund_detail(
        request, program_slug, project_slug, subproject_slug, fund_slug
):
    """
    Display a single fund
    """
    context = {}
    single_fund = Fund.objects.get(slug=fund_slug)
    single_subproject = SubProject.objects.get(slug=subproject_slug)
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
    funds = Fund.objects.filter(sub_project__slug=single_subproject.slug).values()
    subproject = {}
    subproject["name"] = single_subproject.name
    subproject["slug"] = single_subproject.slug
    subproject["approved"] = single_subproject.approved
    subproject["description"] = single_subproject.description
    fund = {}
    fund["amount"] = str(single_fund.amount)
    fund["balance"] = str(single_fund.balance)
    fund["funding_date"] = single_fund.funding_date
    fund["created"] = single_fund.created
    fund["approved"] = single_fund.approved
    fund["slug"] = single_fund.slug
    context["subproject"] = subproject
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
            "subproject": subproject,
        }
    )


@login_required
def update_sub_project_fund(
        request, program_slug, project_slug, subproject_slug, fund_slug
):
    """
    Update a single subproject fund.
    """
    form = FundForm()

    fund_obj = Fund.objects.get(slug=fund_slug)

    if fund_obj is not None:
        if request.method == "POST":
            form = FundForm(request.POST, instance=fund_obj)
            if form.is_valid():
                form.save()
                messages.success(request, "Fund updated successfully.")
                return redirect(
                    reverse_lazy(
                        "tralard:subproject-fund-list",
                        kwargs={
                            "program_slug": program_slug,
                            "project_slug": project_slug,
                            "subproject_slug": subproject_slug,
                        },
                    )
                )
    else:
        messages.error(request, "Fund not found")
        return redirect(
            reverse_lazy(
                "tralard:subproject-fund-list",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                    "subproject_slug": subproject_slug,
                },
            )
        )
    return redirect(
        reverse_lazy(
            "tralard:subproject-fund-list",
            kwargs={
                "program_slug": program_slug,
                "project_slug": project_slug,
                "subproject_slug": subproject_slug,
            },
        )
    )


@login_required(login_url="/login/")
def subproject_fund_delete(
        request, program_slug, project_slug, subproject_slug, fund_slug
):
    """
    Delete a single subproject fund.
    """
    try:
        fund = Fund.objects.get(slug=fund_slug)
        fund.delete()
        messages.success(request, "Subproject Fund deleted successfully")
        return redirect(
            reverse_lazy(
                "tralard:subproject-fund-list",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                    "subproject_slug": subproject_slug,
                },
            )
        )
    except Fund.DoesNotExist:
        messages.error(request, "Subproject Fund not found")
        return redirect(
            reverse_lazy(
                "tralard:subproject-fund-list",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                    "subproject_slug": subproject_slug,
                },
            )
        )


@login_required(login_url="/login/")
def subproject_fund_disbursement_create(
        request, program_slug, project_slug, subproject_slug, fund_slug
):
    """
    Create a single subproject fund disbursement.
    """
    form = DisbursementForm()

    fund_obj = Fund.objects.get(slug=fund_slug)

    if fund_obj is not None:
        if request.method == "POST":
            form = DisbursementForm(request.POST)
            if form.is_valid():
                form.instance.fund = fund_obj
                form.save()
                messages.success(request, "Disbursement created successfully")
                return redirect(
                    reverse_lazy(
                        "tralard:subproject-fund-list",
                        kwargs={
                            "program_slug": program_slug,
                            "project_slug": project_slug,
                            "subproject_slug": subproject_slug,
                        },
                    )
                )
    else:
        messages.error(request, "Fund not found")
        return redirect(
            reverse_lazy(
                "tralard:subproject-fund-list",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                    "subproject_slug": subproject_slug,
                },
            )
        )
    return redirect(
        reverse_lazy(
            "tralard:subproject-fund-list",
            kwargs={
                "program_slug": program_slug,
                "project_slug": project_slug,
                "subproject_slug": subproject_slug,
            },
        )
    )


@login_required(login_url="/login/")
def subproject_disbursement_expenditure_create(
        request, program_slug, project_slug, subproject_slug, fund_slug, disbursement_slug
):
    """
    Create a single subproject fund disbursement expenditure.
    """
    form = ExpenditureForm()

    disbursement_obj = Disbursement.objects.get(slug=disbursement_slug)

    if disbursement_obj is None:
        messages.error(request, "Disbursement not found")
        return redirect(
            reverse_lazy(
                "tralard:subproject-fund-list",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                    "subproject_slug": subproject_slug,
                },
            )
        )
    else:
        if request.method == "POST":
            form = ExpenditureForm(request.POST)
            if form.is_valid():
                form.instance.disbursment = disbursement_obj
                form.save()
                messages.success(request, "Expenditure created successfully")
                return redirect(
                    reverse_lazy(
                        "tralard:subproject-fund-list",
                        kwargs={
                            "program_slug": program_slug,
                            "project_slug": project_slug,
                            "subproject_slug": subproject_slug,
                        },
                    )
                )
            else:
                messages.error(request, form.errors)
                return redirect(
                    reverse_lazy(
                        "tralard:subproject-fund-list",
                        kwargs={
                            "program_slug": program_slug,
                            "project_slug": project_slug,
                            "subproject_slug": subproject_slug,
                        },
                    )
                )
    messages.error(request, "Reached Redirect Block")
    return redirect(
        reverse_lazy(
            "tralard:subproject-fund-list",
            kwargs={
                "program_slug": program_slug,
                "project_slug": project_slug,
                "subproject_slug": subproject_slug,
            },
        )
    )
