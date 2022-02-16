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
            'is_staff',
            'is_superuser',
            'password1',
            'password2'
        ]


class UserUpdateForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "input",
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "input",
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "input",
            }
        ))
    groups = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(),
        choices=ALL_USER_ROLES
    )
    password1 = forms.CharField(
        label='password', 
        widget=forms.PasswordInput(
            attrs={
                'minlength': 6
            }    
        ), 
        required=False
    )
    password2 = forms.CharField(
        label='Confirm password', 
        widget=forms.PasswordInput(
            attrs={
                'minlength': 6
            }    
        ), 
        required=False
    )
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
            'password1',
            'password2',
        ]