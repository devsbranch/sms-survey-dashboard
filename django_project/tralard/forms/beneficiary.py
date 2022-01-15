from mapwidgets.widgets import GooglePointFieldWidget
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import (
    Layout,
    Fieldset,
    HTML,
    Row,
    Column,
)

from django import forms
from django.forms import ModelForm, widgets

from tralard.models.beneficiary import Beneficiary


class BeneficiaryCreateForm(ModelForm):
    class Meta:

        model = Beneficiary
        exclude = ["created",  "slug"]
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
                    Column("above_fourty_five", css_class="form-group col-md-6 mb-0"),
                    Column("sub_project", css_class="form-group col-md-6 mb-0"),
                    Column("ward", css_class="form-group col-md-12 mb-0"),
                    Column("location", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
            ),
        )
