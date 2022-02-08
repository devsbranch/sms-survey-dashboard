from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import (
    Layout,
    Row,
    Column,
)
from crispy_forms.helper import FormHelper
from django_select2.forms import ModelSelect2Widget

from tralard.models.ward import Ward
from tralard.models.province import Province
from tralard.models.district import District
from tralard.models.sub_project import SubProject

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
            "project", 
            "slug", 
            # "ward"
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
                Column("indicators", css_class="form-group col-md-12 mb-0"),
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
        # ward_id = self.cleaned_data["ward"]
        # ward_obj = Ward.objects.get(id=ward_id)
        # instance.ward = ward_obj
        
        if custom_description:
            instance.description = custom_description
        if custom_focus_area:
            instance.focus_area = custom_focus_area
        
        instance.save()
        self.save_m2m()
        return instance
