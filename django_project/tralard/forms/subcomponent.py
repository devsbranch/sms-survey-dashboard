
from django import forms
from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

import crispy_forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from django_select2.forms import ModelSelect2Widget
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    Column,
)

from tralard.models.ward import Ward
from tralard.models.province import Province
from tralard.models.district import District
from tralard.models.subcomponent import Feedback, SubComponent

class SearchForm(forms.Form):
    
    province_id = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        label=_("Province"),
        required=False,
        widget=ModelSelect2Widget(
            attrs={
                'class': 'form-control mb-0 col-md-3 w-3',
                'data-placeholder': '--- Click to select a province ---',
                'data-minimum-input-length': 0,
                },
            model=Province,
            search_fields=['name__icontains'],
        ),
    )

    district_id = forms.ModelChoiceField(
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
            dependent_fields={'province_id': 'province'},
        ),
    )
    
    ward_id = forms.ModelChoiceField(
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
            dependent_fields={'district_id': 'district'},
        ),
    )


class SubComponentForm(ModelForm):
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
        model = SubComponent
        exclude = ["slug", "created"]
        widgets = {
            'name': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'the name given to the subcomponent'
                }
            ),
            'focus_area': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'subcomponent focus area'
                }
            ),
            'description': widgets.Textarea(
                attrs={
                    'class': 'form-control',
                    "placeholder": "write subcomponent description here",
                    "rows": 1,
                    "cols": 2,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ["image_file", "approved", "has_funding", "representative", "focus_area"]:
            self.fields[fieldname].help_text = None

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-6 mb-0"),
                Column("image_file", css_class="form-group col-md-6 mb-0"),
                Column("project", css_class="form-group col-md-6 mb-0"),
                Column("representative", css_class="form-group col-md-6 mb-0"),
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
        instance = super(SubComponentForm, self).save(commit=False)
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
        exclude = ["created", "description", "subcomponent", "slug"]
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
                Column("subcomponent", css_class="form-group col-md-12 mb-0"),
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


class SubComponentFilterForm(crispy_forms.helper.FormHelper):
    form_method = 'GET'
    layout = Layout(
        "name",
        "subcomponent",
        Submit("submit", "Apply Filter", css_class="btn-primary"),
    )
