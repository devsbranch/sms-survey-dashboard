import crispy_forms
from django.contrib.gis import forms

from django.forms import ModelForm, widgets

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    HTML,
    Submit,
    Row,
    Column,
)
from crispy_forms.bootstrap import FormActions

from tralard.models.training import Training

TRAINING_COMPLELTE_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Unkown', 'Unkown'),
]


class TrainingForm(ModelForm):
    custom_completed = forms.ChoiceField(
        label="completed",
        choices=TRAINING_COMPLELTE_CHOICES,
    )

    class Meta:
        model = Training
        exclude = ["id", "slug", "user", "completed"]
        widgets = {
            'start_date': widgets.DateTimeInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': widgets.DateTimeInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.TextInput(attrs={'size': 500, 'title': 'Training Scheddule Notes', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="form-group col-md-12 mb-0"),
                Column("sub_project", css_class="form-group col-md-12 mb-0"),
                Column("training_type", css_class="form-group col-md-12 mb-0"),
                Column("start_date", css_class="form-group col-md-12 mb-0"),
                Column("end_date", css_class="form-group col-md-12 mb-0"),
                Column("moderator", css_class="form-group col-md-12 mb-0"),
                Column("custom_completed", css_class="form-group col-md-12 mb-0"),
                Column("notes", css_class="form-group col-lg-12"),
                css_class="form-row",
            ),
            FormActions(
                Submit("submit", "Submit Details"),
                HTML("<a class='btn btn-danger' href=''>Cancel</a>"),
            ),
        )

    def save(self, commit=True):
        instance = super(TrainingForm, self).save(commit=False)
        custom_completed = self.cleaned_data["custom_completed"]

        if custom_completed.title() == "Yes":
            instance.completed = True

        instance.save()
        return instance


class TrainingFilterForm(crispy_forms.helper.FormHelper):
    class Meta:
        model = Training
        widgets = {
            'start_date': widgets.DateTimeInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': widgets.DateTimeInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="form-group col-md-4 mb-0"),
                Column("sub_project", css_class="form-group col-md-4 mb-0"),
                Column("training_type", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            )
        )
