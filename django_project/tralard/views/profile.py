from django.urls import reverse_lazy
from django.shortcuts import (
    redirect, 
    get_object_or_404,
)
from django.views.generic import (
    UpdateView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tralard.models.profile import Profile
from tralard.forms.profile import ProfileForm
from tralard.utils import user_profile_update_form_validator


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'index.html'
    
    def form_valid(self, form):
        if form.is_valid():
            form.save()
            program_slug = self.request.kwargs.get("program_slug", None)
            project_slug = self.request.kwargs.get("project_slug", None)
            if program_slug and project_slug:
                return redirect(reverse_lazy(
                    "tralard:project-detail", kwargs={
                        "program_slug": program_slug,
                        "project_slug": project_slug,
                    }
                ))
            elif program_slug:
                return redirect(reverse_lazy(
                    "tralard:program-detail",  kwargs={
                        "program_slug": program_slug
                    }
                ))
            return redirect(reverse_lazy(
                "tralard:home"
            ))
