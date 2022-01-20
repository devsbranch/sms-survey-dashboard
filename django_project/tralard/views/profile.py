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
from django.contrib import messages

@login_required(login_url="/login/")
def user_profile_update(request):
    form = ProfileForm()
    training = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "user profile updated successfully!".title())
            return redirect(reverse_lazy("tralard:home"))
