from djmoney.money import Money
from django.forms import ModelForm, widgets
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    HTML,
    Submit,
    Row,
    Column,
)
from crispy_forms.bootstrap import FormActions

from tralard.models.fund import Fund, Disbursement, Expenditure


class FundForm(ModelForm):

    amount = forms.FloatField(required=False, widget=forms.TextInput(
       attrs={'type': 'number','id':'amount','min': '0','step':'0.01'}))
    
    approved = forms.BooleanField(label="approved", initial=False)

    class Meta:
        model = Fund
        exclude = [
            "amount", 
            "created", 
            "balance", 
            "variation", 
            "approved"
        ]
        widgets = {
            'funding_date': widgets.DateInput(
                format=('%m/%d/%Y'), 
                attrs={
                    'class':'form-control', 
                    'type':'date'
                    }
                ),
            }   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row(
                    Column("amount", css_class="form-group col-md-12 mb-0"),
                    Column("currency", css_class="form-group col-md-12 mb-0"),
                    Column("funding_date", css_class="form-group col-md-12 mb-0"),
                    Column("project", css_class="form-group col-md-12 mb-0"),
                    Column("approved", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
            ),
            FormActions(
                Submit("save", "Create Project Fund"),
                HTML('<a class="btn btn-danger" href="/fund/list/">Cancel</a>'),
            ),
        )

    def save(self):
        instance = super(FundForm, self).save(commit=False)
        custom_amount = self.cleaned_data['amount']
        custom_approved = self.cleaned_data['approved']
        instance.amount = custom_amount
        instance.approved = custom_approved
        instance.save()
        return instance

