from django import forms

from django.forms import ModelForm, widgets

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import (
    Layout,
    Fieldset,
    HTML,
    Submit,
    Row,
    Column,
)

from tralard.models.project import Feedback


class FeedbackForm(ModelForm):
    custom_description = forms.CharField(label="Description", widget = forms.Textarea(attrs = {
      'rows': 1,
      'cols': 2,
      'placeholder': 'write your feedback here.'
   }), max_length = 160)
    class Meta:

        model = Feedback
        exclude = ["created", "description", "project", "slug"]
        widgets = {
            'date': widgets.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'type':'date'}),
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
