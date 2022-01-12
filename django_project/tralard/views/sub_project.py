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
import json
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from braces.views import LoginRequiredMixin

from tralard.models.project import Project
from tralard.forms.sub_project import SubProjectForm
from tralard.models.sub_project import SubProject, Indicator

from tralard.utils import user_profile_update_form_validator
from tralard.models import Beneficiary, Project, Program, Ward, SubProject
from tralard.forms import BeneficiaryCreateForm
from tralard.utils import user_profile_update_form_validator

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
            **response_kwargs
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


class SubProjectListView(LoginRequiredMixin, SubProjectMixin, ListView):
    """List view for SubProject."""

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
                    "Sorry! We could not find the project for " "your subproject!"
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
        context = super(SubProjectDetailView, self).get_context_data(**kwargs)
        context["title"] = "sub project"
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
        self.user_profile_utils = user_profile_update_form_validator(
            self.request.POST, self.request.user
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
        context["user_roles"] = self.user_profile_utils[0]
        context["profile"] = self.user_profile_utils[1]
        context["profile_form"] = self.user_profile_utils[2]
        return context
