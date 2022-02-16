# -*- encoding: utf-8 -*-

# Create your views here.
from django.shortcuts import (
    render, 
    redirect, 
    HttpResponse
)
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignUpForm

from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from rolepermissions.decorators import has_role_decorator

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

def register_user(request, extra_arg):
    if request.method == "POST":
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            selected_roles = form.cleaned_data.get("groups", [])
            form.save()
            initial_username = username
            new_user = User.objects.get(username=username)
            if selected_roles:
                new_user.groups.set(selected_roles)
            new_user.save()
            user = authenticate(username=username, password=raw_password)
            
            if extra_arg == 'from-user-management':
                messages.add_message(request, messages.SUCCESS, "New user created successfully")
                return redirect("/accounts/user/management/list/")
        
            messages.add_message(request, messages.SUCCESS, "New user created successfully")
            return redirect("/")
        
        if extra_arg == 'from-user-management':
            messages.add_message(request, messages.ERROR, "Oops! username already exists")
            return redirect('/accounts/user/management/list/')
        
        messages.add_message(request, messages.ERROR, "Oops! username already exists")
        return redirect('/')

@login_required(login_url="/")
def user_delete(request, username):
    user = User.objects.get(username=username)
    user.delete()
    messages.add_message(request, messages.ERROR, f"Delete user '{username}' successfully")
    return redirect('/accounts/user/management/list/')

@has_role_decorator('project_manager')
@login_required(login_url="/")
def user_update(request, pk):
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        form = SignUpForm(request.POST, request.FILES or None ,instance=user) 
        raw_password1 = request.POST.get("password1", user.password)
        raw_password2 = request.POST.get("password2", user.password)
        first_name = request.POST.get("first_name", '')
        last_name = request.POST.get("last_name", '')
        email = request.POST.get("email", '')
        selected_roles = request.POST.getlist("groups", [])
        
        if selected_roles:
            user.groups.clear()
            user.groups.set([original_role.replace(' ', '_').title() for original_role in selected_roles])
        if raw_password1 and raw_password2:
            if raw_password1 == raw_password2:
                user.set_password(raw_password1)
            
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        

        messages.add_message(request, messages.SUCCESS, f"User updated successfully")
        return redirect('/accounts/user/management/list/')
        messages.add_message(request, messages.ERROR, f"Password did not match")
        return redirect('/accounts/user/management/list/')

@has_role_decorator('project_manager')
def list_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None)
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
            messages.add_message(request, messages.SUCCESS, "user created successfully")
            return redirect("/accounts/user/management/list/")

    users = User.objects.all().order_by("-date_joined")
    try:
        username = request.GET.get("username")
        users = User.objects.get(username=username)
    except:
        pass
    try:
        user_paginator = Paginator(users, 7)
        user_page_number = request.GET.get('user_page_number', '')
        user_paginator_list = user_paginator.get_page(user_page_number)
    except:
        user_paginator_list = [users]
    superusers = User.objects.all().filter(is_superuser=True)
    staffs = User.objects.all().filter(is_staff=True)
    context = {
        "all_users": user_paginator_list,
        "users": {
            'count': User.objects.all().count(), 
            'all_users': user_paginator_list
        },
        "superusers": {
            'count': superusers.count(),
            'all_superusers': superusers,
        },
        "staffs": {
            'count': staffs.count(),
            'all_staffs': staffs,
        },
    }
    return render(request, 'accounts/includes/system-user-list.html', context)
