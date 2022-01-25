# -*- encoding: utf-8 -*-

# Create your views here.
from django.shortcuts import (
    render, 
    redirect, 
    HttpResponse
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import LoginForm, SignUpForm

from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def register_user(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            selected_roles = form.cleaned_data.get("groups", [])
            form.save()
            new_user = User.objects.get(username=username)
            if selected_roles:
                new_user.groups.set([original_role.replace(' ', '_').title() for original_role in selected_roles])
            new_user.save()
            user = authenticate(username=username, password=raw_password)
            messages.add_message(request, messages.SUCCESS, "New user created successfully, try again letter.")
            return redirect("/")
        messages.add_message(request, messages.ERROR, "signup failed, try again letter.")
    return render(request, "accounts/register.html", {"form": form})
