# -*- encoding: utf-8 -*-
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from .views import (
    login_view, 
    user_delete,
    user_update,
    register_user,
    list_user,
)
 
urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/<str:extra_arg>/", register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/<str:username>/delete/", user_delete, name="user-delete"),
    path("user/<int:pk>/update/", user_update, name="user-update"),
    path("user/management/list/", list_user, name="user-list"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
