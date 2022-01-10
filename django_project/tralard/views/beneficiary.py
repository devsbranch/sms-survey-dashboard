import json
from django.contrib.auth.decorators import login_required

from django.db.models import fields
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect


from tralard.models import Beneficiary, Project, Program, Ward, SubProject

from tralard.forms import BeneficiaryCreateForm


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


class BeneficiaryOrgListView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Beneficiary
    template_name = "beneficiary/list.html"
    form_class = BeneficiaryCreateForm
    paginate_by = 20
    paginator_class = PaginatorMixin

    def get_success_url(self, **kwargs):
        return reverse(
            "tralard:beneficiary-list",
            kwargs={
                "program_slug": self.kwargs.get("program_slug", None),
                "project_slug": self.kwargs.get("project_slug", None),
            },
        )

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return response

    def get_context_data(self, **kwargs):
        context = super(BeneficiaryOrgListView, self).get_context_data(**kwargs)

        project_slug = self.kwargs.get("project_slug", None)
        beneficiary_objects = Beneficiary.objects.filter(
            sub_project__project__slug=project_slug
        )
        project = Project.objects.get(slug=project_slug)

        page = self.request.GET.get("page", 1)
        paginator = self.paginator_class(beneficiary_objects, self.paginate_by)
        organizations = paginator.page(page)
        context["header"] = "Beneficiaries"
        context["project"] = project
        context["beneficiaries"] = organizations
        return context


@login_required(login_url="/login/")
def beneficiary_detail(request, program_slug, project_slug, beneficiary_slug):
    beneficiary_obj = get_object_or_404(Beneficiary, slug=beneficiary_slug)

    obj_to_dict = model_to_dict(beneficiary_obj)

    ward_id = obj_to_dict["ward"]
    sub_project_id = obj_to_dict["sub_project"]

    obj_to_dict["ward"] = Ward.objects.get(id=ward_id).name
    obj_to_dict["sub_project"] = SubProject.objects.get(id=sub_project_id).name

    try:
        # get cordinates [latitude, longitude]
        obj_to_dict["location"] = obj_to_dict["location"].coords
    except AttributeError:
        pass

    try:
        # get image name and url
        obj_to_dict["logo_url"] = obj_to_dict["logo"].url
        obj_to_dict["logo"] = obj_to_dict["logo"].name
    except ValueError:
        # remove the logo since its an object that can't serialized, because it does not have
        # the name and url.
        obj_to_dict.pop("logo")

    return JsonResponse(obj_to_dict)


@login_required(login_url="/login/")
def beneficiary_update(request, program_slug, project_slug, beneficiary_slug):
    beneficiary_obj = get_object_or_404(Beneficiary, slug=beneficiary_slug)

    form = BeneficiaryCreateForm(instance=beneficiary_obj)
    model_as_dict = form.initial

    image_file_data = model_as_dict["logo"]

    try:
        model_as_dict["logo"] = image_file_data.name
        model_as_dict["logo_image_url"] = image_file_data.url
    except ValueError:
        pass

    try:
        model_as_dict["location"] = model_as_dict["location"].coords
    except AttributeError:
        pass

    if request.method == "POST":
        form = BeneficiaryCreateForm(
            request.POST, request.FILES, instance=beneficiary_obj
        )
        if form.is_valid():
            instance = form.save(commit=False)

            clear_image = request.POST.get("logo-clear", None)
            if clear_image:
                instance.logo = None

            instance.save()
            messages.success(request, "Beneficiary was updated successfully.")
            return redirect(
                reverse_lazy(
                    "tralard:beneficiary-list",
                    kwargs={"program_slug": program_slug, "project_slug": project_slug},
                )
            )

        messages.error(
            request, "An Error occured: Make sure the data in form fields is Valid."
        )
        for field in form:
            for error in field.errors:
                messages.error(request, error)
        return redirect(
            reverse_lazy(
                "tralard:beneficiary-list",
                kwargs={"program_slug": program_slug, "project_slug": project_slug},
            )
        )

    return JsonResponse(model_as_dict)


login_required(login_url="/login/")


def beneficiary_delete(request, program_slug, project_slug, beneficiary_slug):
    beneficiary_obj = get_object_or_404(Beneficiary, slug=beneficiary_slug)

    beneficiary_obj.delete()
    messages.success(request, "The Beneficiary was deleted.")

    return redirect(
        reverse_lazy(
            "tralard:beneficiary-list",
            kwargs={"program_slug": program_slug, "project_slug": project_slug},
        )
    )
