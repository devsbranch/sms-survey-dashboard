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

class TrainingForm(ModelForm):
    
    custom_completed = forms.BooleanField(label="completed", initial=False)
    
    class Meta:

        model = Training
        exclude = ["id", "completed"]
        widgets = {
            'start_date': widgets.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'type':'date'}),
            'end_date': widgets.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'type':'date'}),
            'notes': forms.TextInput(attrs={'size': 500, 'title': 'Training Scheddule Notes',  'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="form-group col-md-12 mb-0 form-control"),
                Column("sub_project", css_class="form-group col-md-12 mb-0 form-control"),
                Column("training_type", css_class="form-group col-md-12 mb-0"),
                Column("start_date", css_class="form-group col-md-12 mb-0"),
                Column("end_date", css_class="form-group col-md-12 mb-0"),
                Column("moderator", css_class="form-group col-md-12 mb-0"),
                Column("completed", css_class="form-group col-md-12 mb-6"),
                Column("custom_completed", css_class="form-group col-md-12 mb-6"),
                Column("notes", css_class="form-group col-lg-12"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Create a Training Schedule"),
                HTML("<a class='btn btn-danger' href='{% url 'tralard:training-list' program_slug project_slug %}'>Cancel</a>"),
            ),
        )
        
    def save(self, commit=True):
        instance = super(TrainingForm, self).save(commit=False)
        custom_completed = self.cleaned_data["custom_completed"]
        instance.completed = custom_completed
        instance.save()
        return instance
