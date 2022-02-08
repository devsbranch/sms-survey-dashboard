
from django import forms
from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

import crispy_forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from django_select2.forms import ModelSelect2Widget
from crispy_forms.layout import (
    Layout,
    Fieldset,
    HTML,
    Submit,
    Row,
    Column,
)

from tralard.models.ward import Ward
from tralard.models.province import Province
from tralard.models.district import District
from tralard.models.project import Feedback, Project

class SearchForm(forms.Form):
    
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        label=_("Province"),
        required=True,
        widget=ModelSelect2Widget(
            attrs={
                'class': 'form-control mb-0 col-md-3',
                'data-placeholder': '--- Click to select a province ---',
                'data-minimum-input-length': 0,
                },
            model=Province,
            search_fields=['name__icontains'],
        ),
    )

    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        label=_("District"),
        required=True,
        widget=ModelSelect2Widget(
            attrs={
                'class': 'form-control mb-0 col-md-3',
                'data-placeholder': '--- Click to select a district ---',
                'data-minimum-input-length': 0,
                },
            model=District,
            search_fields=['name__icontains'],
            dependent_fields={'province': 'province'},
        ),
    )
    
    ward = forms.ModelChoiceField(
        queryset=Ward.objects.all(),
        label=_("Ward"),
        required=True,
        widget=ModelSelect2Widget(
            attrs={
                'class': 'form-control mb-0 col-md-3',
                'data-placeholder': '--- Click to select a ward ---',
                'data-minimum-input-length': 0,
                },
            model=Ward,
            search_fields=['name__icontains'],
            dependent_fields={'district': 'district'},
        ),
    )


class ProjectForm(ModelForm):
    custom_precis = forms.CharField(
        label="Precise summary",
        widget=forms.Textarea(
            attrs={
                "rows": 1,
                "cols": 2,
            }
        ),
        max_length=160,
    )

    class Meta:
        model = Project
        exclude = ["slug", "created"]
        widgets = {
            'name': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'the name given to the project'
                }
            ),
            'focus_area': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'project focus area'
                }
            ),
            'description': widgets.Textarea(
                attrs={
                    'class': 'form-control',
                    "placeholder": "write project description here",
                    "rows": 1,
                    "cols": 2,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ["image_file", "approved", "has_funding", "project_representative", "project_managers",
                          "project_funders", "training_managers", "certification_managers", "focus_area"]:
            self.fields[fieldname].help_text = None

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-6 mb-0"),
                Column("image_file", css_class="form-group col-md-6 mb-0"),
                Column("program", css_class="form-group col-md-6 mb-0"),
                Column("project_representative", css_class="form-group col-md-6 mb-0"),
                Column("project_managers", css_class="form-group col-md-6 mb-0"),
                Column("project_funders", css_class="form-group col-md-6 mb-0"),
                Column("training_managers", css_class="form-group col-md-6 mb-0"),
                Column("certification_managers", css_class="form-group col-md-6 mb-0"),
                Column("approved", css_class="form-group col-md-6 mb-0"),
                Column("has_funding", css_class="form-group col-md-6 mb-0"),
                Column("custom_precis", css_class="form-group col-md-6 mb-0"),
                Column("focus_area", css_class="form-group col-md-6 mb-0"),
                Column("description", css_class="form-group col-md-12 mb-0"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Submit"),
            ),
        )

    def save(self, commit=True):
        instance = super(ProjectForm, self).save(commit=False)
        custom_precis = self.cleaned_data["custom_precis"]
        instance.precis = custom_precis
        instance.save()
        return instance


class FeedbackForm(ModelForm):
    custom_description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
        'rows': 1,
        'cols': 2,
        'placeholder': 'write your feedback here.'
    }), max_length=160)

    class Meta:
        model = Feedback
        exclude = ["created", "description", "project", "slug"]
        widgets = {
            'date': widgets.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="form-group col-md-12 mb-0"),
                Column("date", css_class="form-group col-md-12 mb-0"),
                Column("project", css_class="form-group col-md-12 mb-0"),
                Column("moderator", css_class="form-group col-md-12 mb-0"),
                Column("custom_description", css_class="form-group col-md-12 mb-0 "),
                css_class="form-row has-text-left",
            ),
        )

    def save(self, commit=True):
        instance = super(FeedbackForm, self).save(commit=False)
        custom_description = self.cleaned_data['custom_description']
        instance.description = custom_description
        instance.save()
        return instance


class ProjectFilterForm(crispy_forms.helper.FormHelper):
    form_method = 'GET'
    layout = Layout(
        "name",
        "program",
        Submit("submit", "Apply Filter", css_class="btn-primary"),
    )
