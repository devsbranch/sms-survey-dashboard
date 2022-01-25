# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from tralard.models.profile import Profile
from tralard.forms.profile import ProfileForm
from django.contrib import messages


@login_required(login_url="/login/")
def user_profile_update(request):
    training = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES or None, instance=training)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "user profile updated successfully!".title())
            return redirect(reverse_lazy("tralard:home"))
