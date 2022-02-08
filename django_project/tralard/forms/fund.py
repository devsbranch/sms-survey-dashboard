from django import forms
from django.forms import ModelForm, widgets

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    Column,
)

from tralard.models.fund import Fund, Disbursement, Expenditure


class FundForm(ModelForm):

    amount = forms.FloatField(
        required=False,
        widget=forms.TextInput(
            attrs={"type": "number", "id": "amount", "min": "0", "step": "0.01"}
        ),
    )

    approved = forms.BooleanField(label="approved", initial=False, required=False)

    class Meta:
        model = Fund
        exclude = [
            "amount",
            "created",
            "balance",
            "variation",
            "approved",
            "sub_project",
            "approval_status",
            "approval_status_comment",
            "requested_by",
            "approved_by",
            "approved_date",
        ]
        widgets = {
            "funding_date": widgets.DateInput(
                format=("%m/%d/%Y"),
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
            "approved_date": widgets.DateInput(
                format=("%m/%d/%Y"),
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column(
                    "amount",
                    css_class="form-group col-md-12 mb-0",
                ),
                Column("currency", css_class="form-group col-md-12 mb-0"),
                Column("funding_date", css_class="form-group col-md-12 mb-0"),
                Column("approval_status", css_class="form-group col-md-12 mb-0"),
                Column(
                    "approval_status_comment", css_class="form-group col-md-12 mb-0"
                ),
                Column("requested_by", css_class="form-group col-md-12 mb-0"),
                Column("approved_by", css_class="form-group col-md-12 mb-0"),
                Column("approved_date", css_class="form-group col-md-12 mb-0"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Create Fund"),
            ),
        )

    def save(self):
        instance = super(FundForm, self).save(commit=False)
        custom_amount = self.cleaned_data["amount"]
        instance.amount = custom_amount
        instance.save()
        return instance


class FundApprovalForm(ModelForm):
    amount = forms.FloatField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "number",
                "id": "approved_amount",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    approved = forms.BooleanField(label="approved", initial=False, required=False)

    class Meta:
        model = Fund
        exclude = [
            "amount",
            "created",
            "balance",
            "variation",
            "approved",
            "sub_project",
            "requested_by",
            "currency",
            "funding_date",
            "approved_by",
            "approved",
        ]
        widgets = {
            "approved_date": widgets.DateInput(
                format=("%m/%d/%Y"),
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_tag = False
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Row(
                Column("approval_status", css_class="form-group col-md-12 mb-0"),
                Column("approved_date", css_class="form-group col-md-12 mb-0"),
                Column("amount", css_class="form-group col-md-12 mb-0"),
                Column(
                    "approval_status_comment", css_class="form-group col-md-12 mb-0"
                ),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Update Fund Approval"),
            ),
        )

    def save(self):
        instance = super(FundApprovalForm, self).save(commit=False)
        if instance.approval_status == "APPROVED":
            instance.approved = True
        custom_amount = self.cleaned_data["amount"]
        instance.amount = custom_amount
        instance.save()
        return instance


class DisbursementForm(ModelForm):

    amount = forms.FloatField(
        required=False,
        widget=forms.TextInput(
            attrs={"type": "number", "id": "amount", "min": "0", "step": "0.01"}
        ),
    )

    class Meta:
        model = Disbursement
        exclude = ["amount", "created", "balance", "fund"]
        widgets = {
            "disbursement_date": widgets.DateInput(
                format=("%m/%d/%Y"), attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("amount", css_class="form-group col-md-12 mb-0"),
                Column("currency", css_class="form-group col-md-12 mb-0"),
                Column("disbursement_date", css_class="form-group col-md-12 mb-0"),
                Column("fund", css_class="form-group col-md-12 mb-0"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Create Fund Disbursement"),
            ),
        )

    def save(self):
        instance = super(DisbursementForm, self).save(commit=False)
        custom_amount = self.cleaned_data["amount"]
        instance.amount = custom_amount
        instance.save()
        return instance


class ExpenditureForm(ModelForm):

    amount = forms.FloatField(
        required=False,
        widget=forms.TextInput(
            attrs={"type": "number", "id": "amount", "min": "0", "step": "0.01"}
        ),
    )

    class Meta:
        model = Expenditure
        exclude = ["amount", "created", "disbursment"]
        widgets = {
            "expenditure_date": widgets.DateInput(
                format=("%m/%d/%Y"), attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("amount", css_class="form-group col-md-12 mb-0"),
                Column("currency", css_class="form-group col-md-12 mb-0"),
                Column("expenditure_date", css_class="form-group col-md-12 mb-0"),
                Column("disbursment", css_class="form-group col-md-12 mb-0"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Create Fund Expenditure"),
            ),
        )

    def save(self):
        instance = super(ExpenditureForm, self).save(commit=False)
        custom_amount = self.cleaned_data["amount"]
        instance.amount = custom_amount
        instance.save()
        return instance
