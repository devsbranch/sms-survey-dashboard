# -*- coding: utf-8 -*-

from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from tralard.filters.beneficiary import BeneficiaryFilter
from tralard.forms import BeneficiaryCreateForm
from tralard.models import Beneficiary, SubComponent, Ward, SubProject


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
    # template_name = "beneficiary/list.html"
    form_class = BeneficiaryCreateForm
    paginate_by = 20
    paginator_class = PaginatorMixin

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "tralard:beneficiary-list",
            kwargs={
                "project_slug": self.kwargs.get("project_slug", None),
                "subcomponent_slug": self.kwargs.get("subcomponent_slug", None),
            },
        )

    def form_invalid(self, form):
        response = super().form_invalid(form)
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return response

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "The Beneficiary was created successfully.")
        return redirect(
            reverse_lazy(
                "tralard:subproject-beneficiary",
                kwargs={
                    "project_slug": form.instance.sub_project.subcomponent.project.slug,
                    "subcomponent_slug": form.instance.sub_project.subcomponent.slug,
                    "subproject_slug": form.instance.sub_project.slug,
                },
            )
        )

    def get_context_data(self, **kwargs):
        context = super(BeneficiaryOrgListView, self).get_context_data(**kwargs)

        subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        beneficiary_objects = Beneficiary.objects.filter(
            sub_project__subcomponent__slug=subcomponent_slug
        )
        subcomponent = SubComponent.objects.get(slug=subcomponent_slug)
        page = self.request.GET.get("page", 1)
        paginator = self.paginator_class(beneficiary_objects, self.paginate_by)
        organizations = paginator.page(page)

        try:
            sub_header = f"Showing all Beneficiaries under the <b>{subcomponent.name[:24]}</b> subcomponent."
        except IndexError:
            sub_header = "There are currently no Beneficiaries under this SubComponent."

        context["header"] = "Beneficiaries"
        context["subcomponent"] = subcomponent
        context["beneficiaries"] = organizations
        context["beneficiaries_filter"] = BeneficiaryFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        context["sub_header"] = sub_header
        return context


@login_required(login_url="/login/")
def beneficiary_detail(request, project_slug, subcomponent_slug, beneficiary_slug):
    beneficiary_obj = get_object_or_404(Beneficiary, slug=beneficiary_slug)

    context = {
        "beneficiary": beneficiary_obj,
        "project_slug": project_slug,
        "subcomponent_slug": subcomponent_slug
    }
    return render(request, "includes/beneficiary-detail.html", context)


@login_required(login_url="/login/")
def beneficiary_update(request, project_slug, subcomponent_slug, beneficiary_slug):
    beneficiary_obj = get_object_or_404(Beneficiary, slug=beneficiary_slug)
    form = BeneficiaryCreateForm(instance=beneficiary_obj)

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
                    "tralard:subproject-beneficiary",
                    kwargs={
                        "project_slug": project_slug,
                        "subcomponent_slug": subcomponent_slug,
                        "subproject_slug": beneficiary_obj.sub_project.slug,
                    },
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
                kwargs={"project_slug": project_slug, "subcomponent_slug": subcomponent_slug},
            )
        )

    context = {
        "form": form,
        "project_slug": project_slug,
        "subcomponent_slug": subcomponent_slug,
        "beneficiary": beneficiary_obj
    }
    return render(
        request,
        "beneficiary/update-beneficiary-form.html",
        context
    )

@login_required(login_url="/login/")
def beneficiary_delete(request, project_slug, subcomponent_slug, beneficiary_slug):
    beneficiary_obj = get_object_or_404(Beneficiary, slug=beneficiary_slug)

    beneficiary_obj.delete()
    messages.success(request, "The Beneficiary was deleted.")

    return redirect(
        reverse_lazy(
            "tralard:subproject-beneficiary",
            kwargs={
                "project_slug": project_slug,
                "subcomponent_slug": subcomponent_slug,
                "subproject_slug": beneficiary_obj.sub_project.slug,
            },
        )
    )
