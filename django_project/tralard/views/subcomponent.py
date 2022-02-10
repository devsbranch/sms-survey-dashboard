# -*- coding: utf-8 -*-
from django.contrib import messages
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from tralard.models.project import Project
from tralard.models.subcomponent import SubComponent, Feedback
from tralard.forms.sub_project import SubProjectForm
from tralard.models.sub_project import SubProject, Indicator
from tralard.forms.subcomponent import FeedbackForm, SubComponentForm


@login_required(login_url="/login/")
def subcomponent_create(request, project_slug):
    subcomponent_slug = None
    if request.method == "POST":
        form = SubComponentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save()
            messages.success(request, "The subcomponent was created successfully!")
            subcomponent_slug = instance.slug
            return redirect(
                reverse_lazy(
                    "tralard:subcomponent-detail",
                    kwargs={"project_slug": project_slug, "subcomponent_slug": subcomponent_slug},
                )
            )
        return redirect(
            reverse_lazy(
                "tralard:project-detail",
                kwargs={"project_slug": project_slug, "subcomponent_slug": subcomponent_slug},
            )
        )


@login_required(login_url="/login/")
def subcomponent_update(request, project_slug, subcomponent_slug):
    subcomponent_form = SubComponentForm()
    subcomponent_object = SubComponent.objects.get(slug=subcomponent_slug)
    subcomponent_obj_to_dict = model_to_dict(subcomponent_object)

    try:
        subcomponent_obj_to_dict["image_file"] = subcomponent_object.image_file.name
        subcomponent_obj_to_dict["image_url"] = subcomponent_object.image_file.url
    except ValueError:
        pass

    if request.method == "POST":
        subcomponent_form = SubComponentForm(
            request.POST, request.FILES or None, instance=subcomponent_object
        )
        if subcomponent_form.is_valid():
            instance = subcomponent_form.save(commit=False)
            instance.save()
        messages.success(request, "SubComponent was updated successfully!")
        return redirect(
            reverse_lazy(
                "tralard:subcomponent-detail",
                kwargs={"project_slug": project_slug, "subcomponent_slug": subcomponent_slug},
            )
        )
    else:
        subcomponent_form = get_object_or_404(SubComponent, slug=subcomponent_slug)
    data = {"subcomponent": subcomponent_obj_to_dict}
    return JsonResponse(data)


@login_required(login_url="/login/")
def subcomponent_delete(request, project_slug, subcomponent_slug):
    try:
        subcomponent_object = SubComponent.objects.get(slug=subcomponent_slug)
        subcomponent_object.delete()
        messages.success(request, "SubComponent was deleted successfully!")
    except SubComponent.DoesNotExist:
        pass

    return redirect(
        reverse_lazy("tralard:project-detail", kwargs={"project_slug": project_slug})
    )


class SubComponentDetailView(LoginRequiredMixin, ListView):
    model = SubProject
    context_object_name = "subcomponent"
    template_name = "subcomponent/detail.html"
    form_class = SubProjectForm

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SubComponent, self).get_form_kwargs()
        self.project_slug = self.kwargs.get("project_slug", None)
        self.subcomponent_slug = self.kwargs.get("subcomponent_slug", None)

        self.project = Project.objects.get(slug=self.project_slug)
        self.subcomponent = SubComponent.objects.get(slug=self.subcomponent_slug)

        kwargs.update(
            {
                "user": self.request.user,
                "project": self.project,
                "subcomponent": self.subcomponent,
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
            "tralard:subcomponent-detail",
            kwargs={
                "project_slug": self.object.project.slug,
                "subcomponent_slug": self.object.slug,
            },
        )

    def post(self, request, *args, **kwargs):
        form = SubProjectForm(self.request.POST, self.request.FILES or None)
        if form.is_valid():
            subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
            subcomponent = SubComponent.objects.get(slug=subcomponent_slug)
            form.instance.subcomponent = subcomponent

            form.save()
            messages.success(request, "SubProject was successfully added!")

            return redirect(
                reverse_lazy(
                    "tralard:subproject-manage",
                    kwargs={
                        "project_slug": form.instance.subcomponent.project.slug,
                        "subcomponent_slug": form.instance.subcomponent.slug,
                        "subproject_slug": form.instance.slug,
                    },
                )
            )
        messages.error(
            request,
            "An error occurred when creating the Sub Project. Ensure the data in form fields is correct.",
        )
        for field in form:
            for error in field.errors:
                messages.error(self.request, error)
        return redirect(
            reverse_lazy(
                "tralard:subcomponent-detail",
                kwargs={
                    "project_slug": self.kwargs.get("project_slug", None),
                    "subcomponent_slug": self.kwargs.get("subcomponent_slug", None),
                },
            )
        )

    def get_context_data(self):
        context = super(SubComponentDetailView, self).get_context_data()
        context["title"] = "SubComponent Detail"

        self.subcomponent_slug = self.kwargs.get("subcomponent_slug", None)
        self.subcomponent = SubComponent.objects.get(slug=self.subcomponent_slug)

        self.sub_projects_qs = SubProject.objects.filter(
            subcomponent__slug=self.subcomponent_slug
        )

        self.sub_project_slug = self.kwargs.get("sub_project_slug", None)

        self.sub_project_count = self.sub_projects_qs.count()
        self.all_feedback_qs = Feedback.objects.filter(subcomponent__slug=self.subcomponent_slug)
        self.all_indicator_related_subprojects = Indicator.objects.filter(
            indicator_related_subprojects__in=self.sub_projects_qs
        )
        context["citizen_feedback_list"] = self.all_feedback_qs
        context["subcomponent"] = self.subcomponent
        context["indicators"] = self.all_indicator_related_subprojects
        context["form"] = SubProjectForm
        context["feedback_form"] = FeedbackForm
        context["project_slug"] = self.kwargs.get("project_slug", None)
        context["subcomponent_slug"] = self.kwargs.get("subcomponent_slug", None)
        context["sub_project_list"] = self.sub_projects_qs
        context["total_sub_projects"] = self.sub_project_count
        return context

    def form_valid(self, form):
        form.save()
        return super(SubComponentDetailView, self).form_valid(form)


class SubProjectListView(LoginRequiredMixin, TemplateView):
    template_name = "subcomponent/sub_project_list.html"

    def get_context_data(self):
        context = super(SubProjectListView, self).get_context_data()
        context["title"] = "Sub Project List"
        return context


@login_required(login_url="/login/")
def update_sub_project(request, project_slug, subcomponent_slug, sub_project_slug):
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
                "tralard:subcomponent-detail",
                kwargs={
                    "project_slug": project_slug,
                    "subcomponent_slug": subcomponent_slug,
                },
            )
        )
    return JsonResponse({"data": sub_project_obj_to_dict})


@login_required(login_url="/login/")
def delete_sub_project(request, project_slug, subcomponent_slug, sub_project_slug):
    sub_project = SubProject.objects.get(slug=sub_project_slug)
    sub_project.delete()
    return redirect(
        reverse_lazy(
            "tralard:subcomponent-detail",
            kwargs={
                "project_slug": project_slug,
                "subcomponent_slug": subcomponent_slug,
            },
        )
    )


def create_feedback(request, project_slug, subcomponent_slug):
    form = FeedbackForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        subcomponent = SubComponent.objects.get(slug=subcomponent_slug)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.subcomponent = subcomponent
            instance.save()
            messages.success(request, "Your feedback was added!")
            return redirect(
                reverse_lazy(
                    "tralard:subcomponent-detail",
                    kwargs={"project_slug": project_slug, "subcomponent_slug": subcomponent_slug},
                )
            )
    return redirect(
        reverse_lazy(
            "tralard:subcomponent-detail",
            kwargs={"project_slug": project_slug, "subcomponent_slug": subcomponent_slug},
        )
    )


@login_required(login_url="/login/")
def edit_feedback(request, project_slug, subcomponent_slug, feedback_slug):
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
                "tralard:subcomponent-detail",
                kwargs={"project_slug": project_slug, "subcomponent_slug": subcomponent_slug},
            )
        )
    return JsonResponse({"data": feedback_obj_to_dict})


@login_required(login_url="/login/")
def delete_feedback(request, project_slug, subcomponent_slug, feedback_slug):
    try:
        feedback_obj = Feedback.objects.get(slug=feedback_slug)
        feedback_obj.delete()
    except Feedback.DoesNotExist:
        pass

    return redirect(
        reverse_lazy(
            "tralard:subcomponent-detail",
            kwargs={"project_slug": project_slug, "subcomponent_slug": subcomponent_slug},
        )
    )
