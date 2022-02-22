# -*- coding: utf-8 -*-
__author__ = "Alison Mukoma <mukomalison@gmail.com>"
__date__ = "31/12/2021"
__revision__ = "$Format:%H$"
__copyright__ = "sonlinux bei DigiProphets 2021"
__annotations__ = "Written from 31/12/2021 23:34 AM CET -> 01/01/2022, 00:015 AM CET"

"""
View classes for a SubProject
"""
import datetime
import logging
import re
import reversion

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.http import (
    Http404,
    HttpResponseRedirect,
    JsonResponse,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin
from filer.models import Image as FilerImage
from reversion.models import Version
from reversion.views import RevisionMixin
from rolepermissions.decorators import has_role_decorator

from tralard.filters import (
    BeneficiaryFilter,
    FundFilter,
    TrainingFilter,
)
from tralard.forms import (
    BeneficiaryCreateForm,
    DisbursementForm,
    ExpenditureForm,
    FundApprovalForm,
    FundForm,
    ProgressStatusForm,
    SubProjectForm,
    TrainingForm,
)
from tralard.models import (
    Beneficiary,
    Disbursement,
    Fund,
    FundVersion,
    Photo,
    ProgressStatus,
    SubComponent,
    SubProject,
    Training,
    TrainingType,
    Ward,
)
from tralard.utils import (
    delete_temp_dir,
    delete_temp_file,
    save_to_temp_dir,
    validate_photo_gps_range
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

        :returns: A queryset which to show all versions of subcomponent.
        :rtype: QuerySet
        :raises: Http404
        """
        subcomponent_slug = self.kwargs["subcomponent_slug"]
        subcomponent = get_object_or_404(SubComponent, slug=subcomponent_slug)
        qs = SubProject.objects.all().filter(subcomponent=subcomponent)
        return qs


class SubProjectTrainingListView(LoginRequiredMixin, CreateView):
    model = Training
    form_class = TrainingForm
    template_name = "subcomponent/sub-project-training-list.html"
    sub_project_trainings = None

    def get_success_url(self):
        return reverse_lazy(
            "tralard:subproject-training",
            kwargs={
                "project_slug": self.kwargs.get("project_slug", None),
                "subcomponent_slug": self.kwargs.get("subcomponent_slug", None),
                "subproject_slug": self.kwargs.get("subproject_slug", None),
            },
        )

    def get_context_data(self, **kwargs):
        context = super(SubProjectTrainingListView, self).get_context_data()
        self.subproject_slug = self.kwargs.get("subproject_slug", None)
        self.sub_project_trainings = (
            Training.objects.all().filter(sub_project__slug=self.subproject_slug).all()
        )
        training_filter = TrainingFilter(self.request.GET, queryset=self.get_queryset())

        context["title"] = "Sub Project Trainings"
        context["project_slug"] = self.kwargs.get("project_slug", None)
        context["training_types"] = TrainingType.objects.values_list("name", flat=True)
        context["subcomponent_slug"] = self.kwargs.get("subcomponent_slug", None)
        context["subproject_slug"] = self.kwargs.get("subproject_slug", None)
        context["total_beneficiaries"] = Beneficiary.objects.all().count()
        context["trainings"] = self.sub_project_trainings
        context["trainings_filter"] = training_filter

        self.training_paginator = Paginator(self.sub_project_trainings, 10)
        self.training_page_number = self.request.GET.get("training_page")
        self.training_paginator_list = self.training_paginator.get_page(
            self.training_page_number
        )
        context["trainings"] = self.training_paginator_list
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.is_ajax():
            training_list_html = render_to_string(
                template_name="includes/training-table.html",
                context={"trainings": self.sub_project_trainings},
            )
            data_dict = {
                "training_filter_view": training_list_html,
            }
            return JsonResponse(data=data_dict, safe=False)
        else:
            return response


class SubProjectTrainingUpdateView(LoginRequiredMixin, UpdateView):
    model = Training
    form_class = TrainingForm
    template_name = "includes/sub-project-training-update-modal.html"

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            project_slug = self.kwargs.get("project_slug", None)
            subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
            subproject_slug = self.kwargs.get("subproject_slug", None)

            return redirect(
                reverse_lazy(
                    "tralard:subproject-training",
                    kwargs={
                        "project_slug": project_slug,
                        "subcomponent_slug": subcomponent_slug,
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
            project_slug = self.kwargs.get("project_slug", None)
            subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
            subproject_slug = self.kwargs.get("subproject_slug", None)

            return redirect(
                reverse_lazy(
                    "tralard:subproject-training",
                    kwargs={
                        "project_slug": project_slug,
                        "subcomponent_slug": subcomponent_slug,
                        "subproject_slug": subproject_slug,
                    },
                )
            )


@login_required(login_url="/login/")
def sub_project_training_update(
        request, project_slug, subcomponent_slug, subproject_slug, training_entry_slug
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
                        "project_slug": project_slug,
                        "subcomponent_slug": subcomponent_slug,
                        "subproject_slug": subproject_slug,
                    },
                )
            )
        return redirect(
            reverse_lazy(
                "tralard:subproject-training",
                kwargs={
                    "project_slug": project_slug,
                    "subcomponent_slug": subcomponent_slug,
                },
            )
        )


@login_required(login_url="/login/")
def sub_project_update(request, project_slug, subproject_slug):
    subproject = SubProject.objects.get(slug=subproject_slug)
    if request.method == "POST":
        form = SubProjectForm(request.POST or None, request.FILES, instance=subproject)
        if form.is_valid():
            form.save()
            subproject.save()

        messages.add_message(
            request, messages.SUCCESS, "SubProject updated successfully!"
        )
        return redirect(
            reverse_lazy(
                "tralard:subproject-manage",
                kwargs={
                    "project_slug": project_slug,
                    "subcomponent_slug": subproject.subcomponent.slug
                },
            )
        )


@login_required(login_url="/login/")
def sub_project_training_delete(
        request, project_slug, subcomponent_slug, subproject_slug, training_entry_slug
):
    training = Training.objects.get(slug=training_entry_slug)
    training.delete()
    return redirect(
        reverse_lazy(
            "tralard:subproject-training",
            kwargs={
                "project_slug": project_slug,
                "subcomponent_slug": subcomponent_slug,
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
        subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        context["form"] = SubProjectForm
        context["subcomponent_slug"] = subcomponent_slug
        if subcomponent_slug:
            context["the_subcomponent"] = SubComponent.objects.get(slug=subcomponent_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :returns: A queryset to show all SubProject.

        :param queryset: Optional queryset.
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
            if subcomponent_slug:
                try:
                    subcomponent = SubComponent.objects.get(slug=subcomponent_slug)
                except SubComponent.DoesNotExist:
                    raise Http404(
                        "Sorry! The subcomponent you are requesting a subproject for "
                        "could not be found or you do not have permission to "
                        "view the subproject. Try logging in as a staff member "
                        "if you wish to view it."
                    )
                queryset = (
                    SubProject.objects.all().filter(subcomponent=subcomponent).order_by("name")
                )
                return queryset
            else:
                raise Http404(
                    "Sorry! We could not find the subcomponent for your subproject!"
                )
        else:
            return queryset


class SubProjectDetailView(SubProjectMixin, DetailView):
    """Detail view for SubProject."""

    context_object_name = "sub_project"
    template_name = "subcomponent/sub_project_detail.html"

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because SubProject ids are unique within a Project, we need to make
        sure that we fetch the correct SubProject from the correct Project

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a subcomponent
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            queryset = self.get_queryset()
        subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        sub_project_slug = self.kwargs.get("subproject_slug", None)
        if subcomponent_slug:
            try:
                subcomponent = SubComponent.objects.get(slug=subcomponent_slug)
            except SubComponent.DoesNotExist:
                raise Http404(
                    "The subcomponent you requested a subcateogrty for does not exist."
                )
            try:
                obj = queryset.get(subcomponent=subcomponent, slug=sub_project_slug)
                return obj
            except SubProject.DoesNotExist:
                raise Http404("The subproject you requested does not exist.")
        else:
            raise Http404("Sorry! We could not find your subproject!")

    def get_context_data(self, **kwargs):
        sub_project = self.get_object()
        self.progress_status_qs = ProgressStatus.objects.filter(subproject__name=sub_project.name).order_by("-created")

        progress_status_data = []

        for status in self.progress_status_qs:
            progress_status = {}
            progress_status['id'] = status.id
            progress_status['status'] = status.status
            progress_status['comment'] = status.comment
            progress_status['created'] = status.created
            photos = []
            for pic in status.photo_set.all().order_by('-created'):
                photos.append(pic)

            progress_status['photos'] = photos

            progress_status_data.append(progress_status)

        context = super(SubProjectDetailView, self).get_context_data(**kwargs)
        context["title"] = "Sub Project"
        context["progress_status_qs"] = self.progress_status_qs
        context['progress_status_form'] = ProgressStatusForm
        context['progress_status_data'] = progress_status_data
        context['project_slug'] = self.kwargs.get("project_slug", None)
        context['subcomponent_slug'] = self.kwargs.get("subcomponent_slug", None)
        context['subproject_slug'] = self.kwargs.get("subproject_slug", None)
        return context


@login_required(login_url="/login/")
def progress_status_detail(request, project_slug, subcomponent_slug, subproject_slug, progress_status_id):
    progress_status = ProgressStatus.objects.get(id=progress_status_id)
    context = {
        'progress_status': progress_status,
        "photos": progress_status.photo_set.all(),
        "project_slug": project_slug,
        "subcomponent_slug": subcomponent_slug,
        "subproject_slug": subproject_slug,
    }
    return render(request, 'project/progress_status_detail.html', context)


@login_required
def file_upload_view(request, project_slug, subcomponent_slug, subproject_slug):
    photo = None
    photo_obj = None
    image_url = None
    max_magnitude = 1.5  # distance validation in kilometers accross the sphere portion of the ward

    subproject_obj = SubProject.objects.get(slug=subproject_slug)
    subproject_ward = Ward.objects.get(slug=subproject_obj.ward.slug)
    subproject_ward_location = subproject_ward.location  # get ward coords
    current_time = datetime.datetime.now()
    clean_subproject_name = re.sub(r'\W+', '', f"{subproject_obj.name}")

    if request.method == "POST":
        photos = request.FILES.items()
        status = request.POST.get("status")
        comment = request.POST.get("custom_comment")
        is_completed = True if request.POST.get("custom_is_completed") is "on" else False
        created = request.POST.get("created")

        ProgressStatus(
            status=status,
            comment=comment,
            is_completed=is_completed,
            created=created,
            subproject=subproject_obj,
            timestamp=current_time
        ).save()

        progress_status_obj = ProgressStatus.objects.get(
            timestamp=current_time
        )
        for _, photo in photos:
            if photo:
                image_url = save_to_temp_dir(photo.name, photo)
                temp_saved_photo = FilerImage(file=photo)
                temp_saved_photo.save()
                photo_obj = Photo.objects.create(
                    name=photo.name,
                    image=temp_saved_photo,
                    progress_status=progress_status_obj
                )

                range_is_valid, distance = validate_photo_gps_range(max_magnitude, image_url, subproject_ward_location)
                if range_is_valid:
                    photo_obj.save()
                    delete_temp_file(photo_obj)
                    message = f"{photo_obj.name} suucessfully added to subproject with status of {progress_status_obj.status}."
                    messages.info(request, message)
                else:
                    message = f"The image {photo.name} of {distance} kilometers is not in the allowed ward \n" \
                              f"distance range limit of {max_magnitude}. The image will be discarded."
                    logger.warning(message)
                    messages.warning(request, message)
                    delete_temp_file(photo_obj)
            delete_temp_dir(clean_subproject_name)
    else:
        message = "Something went wrong, image upload was unsuccessful."
        messages.error(request, message)
        raise Http404(message)

    template_name = "project/progress_status_detail.html"
    context = {
        'progress_status': progress_status_obj,
        "photos": progress_status_obj.photo_set.all(),
        "project_slug": project_slug,
        "subcomponent_slug": subcomponent_slug,
        "subproject_slug": subproject_slug,
    }
    return render(request, template_name, context)


# noinspection PyAttributeOutsideInit
class SubProjectDeleteView(LoginRequiredMixin, SubProjectMixin, DeleteView):
    """Delete view for a SubProject."""

    context_object_name = "sub_project"
    template_name = "tralard/sub_project_delete.html"

    def get(self, request, *args, **kwargs):
        """Get the subcomponent_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        self.subcomponent = SubComponent.objects.get(slug=self.subcomponent_slug)
        return super(SubProjectDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the subcomponent_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        self.subcomponent = SubComponent.objects.get(slug=self.subcomponent_slug)
        return super(SubProjectDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the SubProject list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy(
            "subproject-list", kwargs={"subcomponent_slug": self.object.subcomponent.slug}
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
        qs = SubProject.objects.filter(subcomponent=self.subcomponent)
        return qs


# noinspection PyAttributeOutsideInit
class SubProjectCreateView(LoginRequiredMixin, SubProjectMixin, CreateView):
    """Create view for SubProject."""

    context_object_name = "sub_project"
    template_name = "tralard/sub-project-create.html"

    def get_success_url(self):
        """Define the redirect URL

         After successful creation of the object, the User will be redirected
         to the unapproved SubProject list page for the object's parent SubComponent

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy(
            "tralard:subproject-list", kwargs={"subcomponent_slug": self.object.subcomponent.slug}
        )

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SubProjectCreateView, self).get_context_data(**kwargs)
        context["categories"] = self.get_queryset().filter(subcomponent=self.subcomponent)
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
        self.subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        self.subcomponent = SubComponent.objects.get(slug=self.subcomponent_slug)
        kwargs.update({"subcomponent": self.subcomponent})
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
        self.subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        self.subcomponent = SubComponent.objects.get(slug=self.subcomponent_slug)
        kwargs.update({"subcomponent": self.subcomponent})
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SubProjectUpdateView, self).get_context_data(**kwargs)
        context["categories"] = self.get_queryset().filter(subcomponent=self.subcomponent)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to show all subcomponents which
        user created (staff gets all subcomponents)
        :rtype: QuerySet
        """
        subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        subcomponent = SubComponent.objects.get(slug=subcomponent_slug)
        qs = SubProject.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(
                Q(subcomponent=subcomponent)
                & (
                        Q(subcomponent__subcomponent_funders=self.request.user)
                        | Q(subcomponent__subcomponent_managers=self.request.user)
                        | Q(subcomponent__subcomponent_representatives=self.request.user)
                )
            )

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected
        to the SubProject list page for the object's parent SubComponent

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy(
            "tralard:subproject-list", kwargs={"subcomponent_slug": self.object.subcomponent.slug}
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
                "project_slug": self.kwargs.get("project_slug", None),
                "subcomponent_slug": self.kwargs.get("subcomponent_slug", None),
                "subproject_slug": self.kwargs.get("subproject_slug"),
            },
        )

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field in form:
            for error in field.errors:
                messages.error(self.request, "Failure occured trying to save beneficiary form due to: " + error)
        return response

    def form_valid(self, form):
        sub_project = SubProject.objects.get(slug=self.kwargs["subproject_slug"])
        form.instance.sub_project = sub_project
        form.instance.ward = sub_project.ward
        form.save()
        messages.success(self.request, " Successfully added beneficiary!")
        return redirect(
            reverse_lazy(
                "tralard:subproject-beneficiary",
                kwargs={
                    "project_slug": self.kwargs.get("project_slug", None),
                    "subcomponent_slug": self.kwargs.get("subcomponent_slug", None),
                    "subproject_slug": self.kwargs.get("subproject_slug"),
                },
            )
        )

    def get_context_data(self, **kwargs):
        context = super(SubProjectBeneficiaryOrgListView, self).get_context_data(
            **kwargs
        )

        subproject_slug = self.kwargs.get("subproject_slug", None)
        subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        beneficiary_objects = Beneficiary.objects.filter(
            sub_project__slug=subproject_slug
        )
        subcomponent = SubComponent.objects.get(slug=subcomponent_slug)

        # Just get the subproject name from one beneficiary since we are filtering
        # by a subproject.
        try:
            sub_header = f"Showing all Beneficiaries under the <b>{beneficiary_objects[0].sub_project.name}</b> Sub Project."
        except IndexError:
            sub_header = "There are currently no Beneficiaries under this Sub-Project."

        page = self.request.GET.get("page", 1)
        paginator = self.paginator_class(beneficiary_objects, self.paginate_by)
        organizations = paginator.page(page)
        context["header"] = "Beneficiaries"
        context["subcomponent"] = subcomponent
        context["subproject_slug"] = subproject_slug
        context["beneficiaries"] = organizations
        context["beneficiary_filter"] = BeneficiaryFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        context["sub_header"] = sub_header
        return context


class SubProjectFundListAndCreateView(RevisionMixin, LoginRequiredMixin, CreateView):
    """
    Create a new Sub Project Fund
    """

    model = Fund
    form_class = FundForm
    disbursement_form_class = DisbursementForm
    expenditure_form_class = ExpenditureForm
    context_object_name = "project"
    fund_approval_form_class = FundApprovalForm
    template_name = "subcomponent/fund-list.html"

    funds = None

    def get_success_url(self):
        """
        After successful creation of the object, the User will be redirected
        to the SubProject list page for the object's parent SubComponent
        """
        return reverse_lazy(
            "tralard:subproject-fund-list",
            kwargs={
                "project_slug": self.object.sub_project.subcomponent.project.slug,
                "subcomponent_slug": self.object.sub_project.subcomponent.slug,
                "subproject_slug": self.object.sub_project.slug,
            },
        )

    def get_context_data(self, **kwargs):
        context = super(SubProjectFundListAndCreateView, self).get_context_data(
            **kwargs
        )
        self.project_slug = self.kwargs["project_slug"]
        self.subproject_slug = self.kwargs["subproject_slug"]

        self.sub_project = SubProject.objects.get(slug=self.subproject_slug)
        self.funds = Fund.objects.filter(sub_project__slug=self.subproject_slug)

        context["sub_project"] = self.sub_project
        context["funds"] = self.funds
        context["funds_filter"] = FundFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        context["fund_title"] = "add sub project fund"
        context["modal_display"] = "none"
        context["form"] = self.form_class
        context["disbursement_form"] = self.disbursement_form_class
        context["expenditure_form"] = self.expenditure_form_class
        context["fund_approval_form"] = self.fund_approval_form_class
        context["disbursement_title"] = "create fund disbursement"
        context["title"] = "funds"
        return context

    def form_valid(self, form):
        sub_project_object = SubProject.objects.get(slug=self.kwargs["subproject_slug"])
        if form.is_valid():
            with reversion.create_revision():
                form.instance.sub_project = sub_project_object
                form.instance.approval_status = "PENDING"
                form.instance.requested_by = self.request.user
                form.save()
                reversion.set_user(self.request.user)
                reversion.set_comment(
                    "Requested Sub Project Fund: " + str(form.instance.amount)
                )
                reversion.add_meta(
                    FundVersion,
                    initial_amount=form.instance.amount,
                    approved=form.instance.approved,
                    approval_status=form.instance.approval_status,
                    approval_status_comment=form.instance.approval_status_comment,
                    funding_date=form.instance.funding_date,
                    requested_by=form.instance.requested_by,
                    approved_by=form.instance.approved_by,
                    approved_date=form.instance.approved_date,
                )
                messages.success(self.request, "Fund created sucessfully")
                return super(SubProjectFundListAndCreateView, self).form_valid(form)
        else:
            messages.error(self.request, "Error creating fund")
            return self.form_invalid(form)


@has_role_decorator(["project_manager", "subcomponent_manager", "fund_manager"])
def fund_approval_view(request, project_slug, subcomponent_slug, subproject_slug, fund_slug):
    """
    Approve or reject a fund request
    """
    form = FundApprovalForm()

    fund_obj = Fund.objects.get(slug=fund_slug)

    if fund_obj is None:
        messages.error(request, "Error updating fund approval status")
        return redirect(
            reverse_lazy(
                "tralard:subproject-fund-list",
                kwargs={
                    "project_slug": project_slug,
                    "subcomponent_slug": subcomponent_slug,
                    "subproject_slug": subproject_slug,
                },
            )
        )
    else:
        if request.method == "POST":
            form = FundApprovalForm(request.POST, instance=fund_obj)
            if form.is_valid():
                with reversion.create_revision():
                    form.instance.approved_by = request.user
                    form.save()
                    reversion.set_user(request.user)
                    reversion.set_comment(
                        str(form.instance.slug) + " Fund Approval Status Updated"
                    )

                    messages.success(request, "Fund Approval Status Updated")
                    return redirect(
                        reverse_lazy(
                            "tralard:subproject-fund-list",
                            kwargs={
                                "project_slug": project_slug,
                                "subcomponent_slug": subcomponent_slug,
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
                            "project_slug": project_slug,
                            "subcomponent_slug": subcomponent_slug,
                            "subproject_slug": subproject_slug,
                        },
                    )
                )
    messages.error(request, "Error updating fund approval status")
    return redirect(
        reverse_lazy(
            "tralard:subproject-fund-list",
            kwargs={
                "project_slug": project_slug,
                "subcomponent_slug": subcomponent_slug,
                "subproject_slug": subproject_slug,
            },
        )
    )


@login_required
def subproject_fund_detail(
        request, project_slug, subcomponent_slug, subproject_slug, fund_slug
):
    """
    Display a single fund
    """
    context = {}
    single_fund = Fund.objects.get(slug=fund_slug)
    version_list = Version.objects.get_for_object(single_fund)
    versions = []
    for version in version_list:
        versions.append(version.serialized_data)
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
    subproject = {
        "name": single_subproject.name,
        "slug": single_subproject.slug,
        "approved": single_subproject.approved,
        "description": single_subproject.description,
    }
    fund = {
        "amount": str(single_fund.amount),
        "balance": str(single_fund.balance),
        "funding_date": single_fund.funding_date,
        "created": single_fund.created,
        "approved": single_fund.approved,
        "slug": single_fund.slug,
    }
    context["subproject"] = subproject
    context["disbursements"] = disbursements
    context["title"] = "Fund details"
    context["funds"] = funds
    context["form"] = FundForm
    context["modal_display"] = "block"
    fund["versions"] = versions
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
        request, project_slug, subcomponent_slug, subproject_slug, fund_slug
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
                with reversion.create_revision():
                    form.save()
                    fund_obj.save()
                    reversion.set_user(request.user)
                    reversion.set_comment(form.instance.slug + " Fund Updated")
                    messages.success(request, "Fund updated successfully.")
                    return redirect(
                        reverse_lazy(
                            "tralard:subproject-fund-list",
                            kwargs={
                                "project_slug": project_slug,
                                "subcomponent_slug": subcomponent_slug,
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
                    "project_slug": project_slug,
                    "subcomponent_slug": subcomponent_slug,
                    "subproject_slug": subproject_slug,
                },
            )
        )
    return redirect(
        reverse_lazy(
            "tralard:subproject-fund-list",
            kwargs={
                "project_slug": project_slug,
                "subcomponent_slug": subcomponent_slug,
                "subproject_slug": subproject_slug,
            },
        )
    )


@login_required(login_url="/login/")
def subproject_fund_delete(
        request, project_slug, subcomponent_slug, subproject_slug, fund_slug
):
    """
    Delete a single subproject fund.
    """
    try:
        fund = Fund.objects.get(slug=fund_slug)
        with reversion.create_revision():
            fund.delete()
            reversion.set_user(request.user)
            reversion.set_comment(fund.slug + " Fund Deleted")
            messages.success(request, "Subproject Fund deleted successfully")
            return redirect(
                reverse_lazy(
                    "tralard:subproject-fund-list",
                    kwargs={
                        "project_slug": project_slug,
                        "subcomponent_slug": subcomponent_slug,
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
                    "project_slug": project_slug,
                    "subcomponent_slug": subcomponent_slug,
                    "subproject_slug": subproject_slug,
                },
            )
        )


@login_required(login_url="/login/")
def subproject_fund_disbursement_create(
        request, project_slug, subcomponent_slug, subproject_slug, fund_slug
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
                fund_obj.save()
                messages.success(request, "Disbursement created successfully")
                return redirect(
                    reverse_lazy(
                        "tralard:subproject-fund-list",
                        kwargs={
                            "project_slug": project_slug,
                            "subcomponent_slug": subcomponent_slug,
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
                    "project_slug": project_slug,
                    "subcomponent_slug": subcomponent_slug,
                    "subproject_slug": subproject_slug,
                },
            )
        )
    return redirect(
        reverse_lazy(
            "tralard:subproject-fund-list",
            kwargs={
                "project_slug": project_slug,
                "subcomponent_slug": subcomponent_slug,
                "subproject_slug": subproject_slug,
            },
        )
    )


@login_required(login_url="/login/")
def subproject_disbursement_expenditure_create(
        request, project_slug, subcomponent_slug, subproject_slug, fund_slug, disbursement_slug
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
                    "project_slug": project_slug,
                    "subcomponent_slug": subcomponent_slug,
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
                disbursement_obj.save()
                messages.success(request, "Expenditure created successfully")
                return redirect(
                    reverse_lazy(
                        "tralard:subproject-fund-list",
                        kwargs={
                            "project_slug": project_slug,
                            "subcomponent_slug": subcomponent_slug,
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
                            "project_slug": project_slug,
                            "subcomponent_slug": subcomponent_slug,
                            "subproject_slug": subproject_slug,
                        },
                    )
                )
    messages.error(request, "An Error Occurred while creating Expenditure")
    return redirect(
        reverse_lazy(
            "tralard:subproject-fund-list",
            kwargs={
                "project_slug": project_slug,
                "subcomponent_slug": subcomponent_slug,
                "subproject_slug": subproject_slug,
            },
        )
    )
