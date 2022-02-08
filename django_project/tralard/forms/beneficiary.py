
from django import forms
from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Row,
    Column,
)

from django_select2.forms import ModelSelect2Widget
from mapwidgets.widgets import GooglePointFieldWidget

from tralard.models.ward import Ward
from tralard.models.province import Province
from tralard.models.district import District
from tralard.models.beneficiary import Beneficiary


class BeneficiaryCreateForm(ModelForm):

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

    class Meta:

        model = Beneficiary
        exclude = [
            "created",  
            "slug", 
            "location",
            "sub_project"
        ]
        widgets = {
            "location": GooglePointFieldWidget,
            "registered_date": widgets.DateInput(
                format=("%m/%d/%Y"), attrs={
                    "class": "form-control", 
                    "type": "date"
                    }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "cols": 2,
                    "title": "The Beneficiary organization description",
                    "required": False,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Fieldset(
                "Beneficiary Info",
                Row(
                    Column("name", css_class="form-group col-md-6 mb-0"),
                    Column("org_type", css_class="form-group col-md-6 mb-0"),
                    Column("logo", css_class="form-group col-md-6 mb-0"),
                    Column("cell", css_class="form-group col-md-6 mb-0"),
                    Column("email", css_class="form-group col-md-6 mb-0"),
                    Column("registered_date", css_class="form-group col-md-6 mb-0"),
                    Column("description", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Other Meta Data",
                Row(
                    Column("total_beneficiaries", css_class="form-group col-md-6 mb-0"),
                    Column("total_females", css_class="form-group col-md-6 mb-0"),
                    Column("total_males", css_class="form-group col-md-6 mb-0"),
                    Column("total_hhs", css_class="form-group col-md-6 mb-0"),
                    Column("female_hhs", css_class="form-group col-md-6 mb-0"),
                    Column("below_sixteen", css_class="form-group col-md-6 mb-0"),
                    Column("sixteen_to_thirty", css_class="form-group col-md-6 mb-0"),
                    Column(
                        "thirty_to_fourty_five", css_class="form-group col-md-6 mb-0"
                    ),
                    Column("above_fourty_five", css_class="form-group col-md-12 mb-0"),
                    Column("province", css_class="form-group col-md-12 mb-0"),
                    Column("district", css_class="form-group col-md-12 mb-0"),
                    Column("ward", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
            ),
        )
