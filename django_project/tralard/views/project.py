from typing import List
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.core import serializers

import json

from tralard.models.program import Program
from tralard.models.project import Project, Feedback, Representative
from tralard.models.sub_project import SubProject, Indicator

from tralard.forms.sub_project import SubProjectForm
from tralard.forms.project import FeedbackForm


class ProjectDetailView(LoginRequiredMixin, ListView):
    model = SubProject
    context_object_name = "project"
    template_name = "project/detail.html"
    form_class = SubProjectForm

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(Project, self).get_form_kwargs()
        self.program_slug = self.kwargs.get("program_slug", None)
        self.project_slug = self.kwargs.get("project_slug", None)

        self.program = Program.objects.get(slug=self.program_slug)
        self.project = Project.objects.get(slug=self.project_slug)

        kwargs.update(
            {
                "user": self.request.user,
                "program": self.program,
                "project": self.project,
            }
        )

        return kwargs

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the SubProject list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse_lazy(
            "tralard:project-detail",
            kwargs={
                "program_slug": self.object.program.slug,
                "project_slug": self.object.slug,
            },
        )

    def post(self, request, *args, **kwargs):
        self.status_form = SubProjectForm(self.request.POST, self.request.FILES or None)
        if self.status_form.is_valid():
            self.status_form.save()
            messages.success(request, "Your SubProject was added!")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            ...
        else:
            messages.error(request, "Some thing went wrong")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def get_context_data(self):
        context = super(ProjectDetailView, self).get_context_data()
        context["title"] = "Project Detail"

        self.project_slug = self.kwargs.get("project_slug", None)
        self.project = Project.objects.get(slug=self.project_slug)

        self.sub_projects_qs = SubProject.objects.filter(
            project__slug=self.project_slug
        )

        self.sub_project_slug = self.kwargs.get("sub_project_slug", None)

        self.sub_project_count = self.sub_projects_qs.count()
        self.all_feedback_qs = Feedback.objects.filter(project__slug=self.project_slug)
        self.all_subproject_indicators = Indicator.objects.filter(
            subproject_indicators__in=self.sub_projects_qs
        )
        context["citizen_feedback_list"] = self.all_feedback_qs
        context["project"] = self.project
        context["indicators"] = self.all_subproject_indicators
        context["form"] = SubProjectForm
        context["feedback_form"] = FeedbackForm
        context["program_slug"] = self.kwargs.get("program_slug", None)
        context["project_slug"] = self.kwargs.get("project_slug", None)
        context["sub_project_list"] = self.sub_projects_qs
        context["total_sub_projects"] = self.sub_project_count

        return context

    def form_valid(self, form):
        form.save()
        return super(ProjectDetailView, self).form_valid(form)


class SubProjectListView(LoginRequiredMixin, TemplateView):
    template_name = "project/sub_project_list.html"

    def get_context_data(self):
        context = super(SubProjectListView, self).get_context_data()
        context["title"] = "Sub Project List"
        return context


class SubProjectDetailView(LoginRequiredMixin, TemplateView):
    template_name = "project/sub_project_detail.html"

    def get_context_data(self):
        context = super(SubProjectDetailView, self).get_context_data()
        context["title"] = "Sub Project Detail"
        return context


@login_required(login_url="/login/")
def update_sub_project(request, program_slug, project_slug, sub_project_slug):
    sub_project_obj = SubProject.objects.get(slug=sub_project_slug)
    sub_project_obj_to_dict = model_to_dict(sub_project_obj)

    indicators = [
        model_to_dict(indicator) for indicator in sub_project_obj_to_dict["indicators"]
    ]

    try:
        sub_project_obj_to_dict["image_file"] = sub_project_obj.image_file.name
        sub_project_obj_to_dict["image_url"] = sub_project_obj.image_file.url
    except ValueError:
        pass

    sub_project_obj_to_dict["indicators"] = indicators
    sub_project_obj_to_dict["total_num_of_indicators"] = len(indicators)

    if request.method == "POST":
        form = SubProjectForm(
            request.POST, request.FILES or None, instance=sub_project_obj
        )
        if form.is_valid():
            form.save()
        messages.success(request, "Your SubProject was updated!")
        return redirect(
            reverse_lazy(
                "tralard:project-detail",
                kwargs={
                    "program_slug": program_slug,
                    "project_slug": project_slug,
                },
            )
        )
    return JsonResponse({"data": sub_project_obj_to_dict})


@login_required(login_url="/login/")
def delete_sub_project(request, program_slug, project_slug, sub_project_slug):
    sub_project = SubProject.objects.get(slug=sub_project_slug)
    sub_project.delete()
    return redirect(
        reverse_lazy(
            "tralard:project-detail",
            kwargs={
                "program_slug": program_slug,
                "project_slug": project_slug,
            },
        )
    )


def create_feedback(request, program_slug, project_slug):
    form = FeedbackForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        project = Project.objects.get(slug=project_slug)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            instance.save()
            messages.success(request, "Your feedback was added!")
            return redirect(
                reverse_lazy(
                    "tralard:project-detail",
                    kwargs={"program_slug": program_slug, "project_slug": project_slug},
                )
            )
    return redirect(
        reverse_lazy(
            "tralard:project-detail",
            kwargs={"program_slug": program_slug, "project_slug": project_slug},
        )
    )


@login_required(login_url="/login/")
def edit_feedback(request, program_slug, project_slug, feedback_slug):
    form = FeedbackForm()

    feedback_obj = Feedback.objects.get(slug=feedback_slug)
    feedback_obj_to_dict = model_to_dict(feedback_obj)
    try:
        feedback_obj_to_dict[
            "moderator_name"
        ] = f"{feedback_obj.moderator.first_name} {feedback_obj.moderator.last_name}"
    except AttributeError:
        pass

    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=feedback_obj)
        if form.is_valid():
            form.save()
        messages.success(request, "Your feedback was updated!")
        return redirect(
            reverse_lazy(
                "tralard:project-detail",
                kwargs={"program_slug": program_slug, "project_slug": project_slug},
            )
        )
    return JsonResponse({"data": feedback_obj_to_dict})


@login_required(login_url="/login/")
def delete_feedback(request, program_slug, project_slug, feedback_slug):
    try:
        feedback_obj = Feedback.objects.get(slug=feedback_slug)
        feedback_obj.delete()
    except Feedback.DoesNotExist:
        pass

    return redirect(
        reverse_lazy(
            "tralard:project-detail",
            kwargs={"program_slug": program_slug, "project_slug": project_slug},
        )
    )
