# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from tralard.filters.training import TrainingFilter
from tralard.models.training import Training
from tralard.forms.training import TrainingForm
from tralard.models.beneficiary import Beneficiary


class TrainingListView(LoginRequiredMixin, CreateView):
    model = Training
    form_class = TrainingForm
    template_name = "training/list.html"

    def get_success_url(self):
        return reverse_lazy(
            "tralard:training-list",
            kwargs={
                "project_slug": self.kwargs.get("project_slug", None),
                "subcomponent_slug": self.kwargs.get("subcomponent_slug", None),
            },
        )

    def get_context_data(self):
        context = super(TrainingListView, self).get_context_data()
        self.trainings = Training.objects.all()
        context["title"] = "Training"
        context["total_beneficiaries"] = Beneficiary.objects.all().count()
        context["project_slug"] = self.kwargs.get("project_slug", None)
        context["subcomponent_slug"] = self.kwargs.get("subcomponent_slug", None)
        training_filter = TrainingFilter(self.request.GET, queryset=self.get_queryset())

        self.training_paginator = Paginator(self.trainings, 10)
        self.training_page_number = self.request.GET.get("training_page")
        self.training_paginator_list = self.training_paginator.get_page(
            self.training_page_number
        )

        context["trainings_filter"] = training_filter
        context["trainings"] = self.training_paginator.get_page(
            self.training_page_number
        )
        return context


@login_required(login_url="/login/")
def training_delete(request, project_slug, subcomponent_slug, training_entry_slug):
    training = Training.objects.get(slug=training_entry_slug)
    training.delete()
    return redirect(
        reverse_lazy(
            "tralard:training-list",
            kwargs={
                "project_slug": project_slug,
                "subcomponent_slug": subcomponent_slug,
            },
        )
    )


@login_required(login_url="/login/")
def training_update(request, project_slug, subcomponent_slug, training_entry_slug):
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
                        "project_slug": project_slug,
                        "subcomponent_slug": subcomponent_slug,
                    },
                )
            )
        return redirect(
            reverse_lazy(
                "tralard:training-list",
                kwargs={
                    "project_slug": project_slug,
                    "subcomponent_slug": subcomponent_slug,
                },
            )
        )


# temporal view for previewing templates
@login_required(login_url="/login/")
def template_testing(request):
    return render(request, "tralard/dashboard-datatable-advanced.html")
