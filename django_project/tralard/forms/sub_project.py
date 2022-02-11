from django import forms
from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import (
    Layout,
    Row,
    Column,
)
from crispy_forms.helper import FormHelper
from django_select2.forms import ModelSelect2Widget, Select2TagWidget

from tralard.models.ward import Ward
from tralard.models.province import Province
from tralard.models.district import District
from tralard.models.sub_project import (
    SubProject, 
    ProgressStatus, 
)


class SubProjectForm(ModelForm):
    
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        label=_("Province"),
        required=False,
        widget=ModelSelect2Widget(
            attrs={
                'class': 'form-control mb-0 col-md-12',
                'data-placeholder': '--- Select a province ---',
                'data-minimum-input-length': 0,
                },
            model=Province,
            search_fields=['name__icontains'],
        ),
    )

    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        label=_("District"),
        required=False,
        widget=ModelSelect2Widget(
            attrs={
                "cols": 15,
                'class': 'form-control',
                'data-placeholder': '--- select a related district ---',
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
        required=False,
        widget=ModelSelect2Widget(
            attrs={
                'class': 'form-control mb-0 col-md-12',
                'data-placeholder': '--- Select a related ward ---',
                'data-minimum-input-length': 0,
                },
            model=Ward,
            search_fields=['name__icontains'],
            dependent_fields={'district': 'district'},
        ),
    )

    custom_description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 1,
                "cols": 2,
                "placeholder": "write subproject description here",
            }
        ),
        max_length=160,
    )

    custom_focus_area = forms.CharField(
        label="Focus Area",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 1,
                "cols": 2,
                "placeholder": "write subproject focus area here",
            }
        ),
        max_length=160,
    )

    class Meta:

        model = SubProject
        exclude = [
            "created", 
            "description", 
            "focus_area", 
            "subcomponent", 
            "slug",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-12 mb-0"),
                Column("supervisor", css_class="form-group col-md-12 mb-0"),
                Column("size", css_class="form-group col-md-12 mb-0"),
                Column("subproject_managers", css_class="form-group col-md-12 mb-0"),
                Column("province", css_class="form-group col-md-12 mb-0"),
                Column("district", css_class="form-group col-md-12 mb-0"),
                Column("ward", css_class="form-group col-md-12 mb-0"),
                Column("approved", css_class="form-group col-md-12 mb-0"),
                Column("image_file", css_class="form-group col-md-12 mb-0"),
                Column("custom_description", css_class="form-group col-md-12 mb-0"),
                Column("custom_focus_area", css_class="form-group col-md-12 mb-0"),
                css_class="form-row",
            ),
        )

    def save(self, commit=True):
        instance = super(SubProjectForm, self).save(commit=False)
        custom_description = self.cleaned_data["custom_description"]
        custom_focus_area = self.cleaned_data["custom_focus_area"]
        if custom_description:
            instance.description = custom_description
        if custom_focus_area:
            instance.focus_area = custom_focus_area
        instance.save()
        return instance

class ProgressStatusForm(ModelForm):
    custom_is_completed = forms.BooleanField(label="completed", initial=False, required=False)
    custom_comment = forms.CharField(
        label="Progress Status Commment",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 1,
                "cols": 2,
                "placeholder": "write subproject progress comment here",
            }
        ),
        max_length=160,
    )
    class Meta:
        model = ProgressStatus
        exclude= [
            "photos",
            "comment", 
            "subproject", 
            "is_completed"
        ]
        widgets = {
            "created": widgets.DateInput(
                format=("%m/%d/%Y"), attrs={"class": "form-control", "type": "date"}
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column("status", css_class="form-group col-md-12 mb-0"),
                Column("custom_comment", css_class="form-group col-md-12 mb-0"),
                Column("custom_is_completed", css_class="form-group col-md-12 mb-0"),
                Column("created", css_class="form-group col-md-12 mb-0"),
                css_class="form-row",
            ),
        )

    def save(self, commit=True):
        instance = super(ProgressStatus, self).save(commit=False)
        custom_comment = self.cleaned_data["custom_comment"]
        custom_is_completed = self.cleaned_data["custom_is_completed"]
        if custom_comment:
            instance.comment = custom_comment
        if custom_is_completed:
            instance.is_completed = custom_is_completed
        instance.save()
        self.save_m2m()
        return instance
