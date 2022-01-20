from re import template
import json

from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
)
from django.shortcuts import (
    HttpResponse,
    redirect,
    render,
    get_object_or_404,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core import serializers

from tralard.models.beneficiary import Beneficiary
from tralard.forms.training import TrainingForm
from tralard.forms.profile import ProfileForm
from tralard.models.training import Training
from tralard.models.profile import Profile


class TrainingListView(LoginRequiredMixin, CreateView):
    model = Training
    form_class = TrainingForm
    template_name = "training/list.html"

    def get_success_url(self):
        return reverse_lazy(
            "tralard:training-list",
            kwargs={
                "program_slug": self.kwargs.get("program_slug", None),
                "project_slug": self.kwargs.get("project_slug", None),
            },
        )

    def get_context_data(self):
        context = super(TrainingListView, self).get_context_data()
        self.trainings = Training.objects.all()
        context["title"] = "Training"
        context["total_beneficiaries"] = Beneficiary.objects.all().count()
        context["program_slug"] = self.kwargs.get("program_slug", None)
        context["project_slug"] = self.kwargs.get("project_slug", None)
            
        self.training_paginator = Paginator(self.trainings, 10)
        self.training_page_number = self.request.GET.get("training_page")
        self.training_paginator_list = self.training_paginator.get_page(
            self.training_page_number
        )
        context["trainings"] = self.training_paginator.get_page(self.training_page_number)
        return context


@login_required(login_url="/login/")
def training_delete(request, program_slug, project_slug, training_entry_slug):
    training = Training.objects.get(slug=training_entry_slug)
    training.delete()
    return redirect(
        reverse_lazy(
            "tralard:training-list",
            kwargs={
                "program_slug": program_slug,
                "project_slug": project_slug,
            },
        )
    )


@login_required(login_url="/login/")
def training_update(request, program_slug, project_slug, training_entry_slug):
    form = TrainingForm()
    training = Training.objects.get(slug=training_entry_slug)
    if request.method == "POST":
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect(
                reverse_lazy(
                    "tralard:training-list",
                    kwargs={
                        "program_slug": program_slug,
                        "project_slug": project_slug,
                    },
                )
            )
        return redirect(
            reverse_lazy(
                "tralard:training-list",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                },
            )
        )


# temporal view for previewing templates
@login_required(login_url="/login/")
def template_testing(request):
    return render(request, "tralard/dashboard-datatable-variationss.html")
