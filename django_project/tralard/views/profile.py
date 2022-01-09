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

from tralard.models.profile import Profile
from tralard.forms.profile import ProfileForm
from tralard.utils import current_user_roles

    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'tralard/index.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy(
                "tralard:home"
            ))
    