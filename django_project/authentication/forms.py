# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tralard.utils import get_available_roles

ALL_USER_ROLES = []
role_storage = get_available_roles()
for cleaned_role_appearance in enumerate(role_storage):
    original_role_appearance = cleaned_role_appearance[1].replace(' ', "_").lower()
    ALL_USER_ROLES.append(
        (f"{cleaned_role_appearance[0]+1}", cleaned_role_appearance[1])
    )
    
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "input"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "input"
            }
        ))


class SignUpForm(UserCreationForm):
    groups = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(),
        choices=ALL_USER_ROLES
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
        ]
