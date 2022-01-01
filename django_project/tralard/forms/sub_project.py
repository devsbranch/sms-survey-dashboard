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

from tralard.models.sub_project import SubProject


class SubProjectForm(ModelForm):
    class Meta:

        model = SubProject
        exclude = ["created"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row(
                    Column("name", css_class="form-group col-md-6 mb-0"),
                    Column("size", css_class="form-group col-md-6 mb-0"),
                    Column("supervisor", css_class="form-group col-md-6 mb-0"),
                    Column("project", css_class="form-group col-md-6 mb-0"),
                    Column("indicators", css_class="form-group col-md-6 mb-0"),
                    Column("subproject_managers", css_class="form-group col-md-6 mb-0"),
                    Column("approved", css_class="form-group col-md-12 mb-0"),
                    Column("image_file", css_class="form-group col-md-12 mb-0"),
                    Column("description", css_class="form-group col-md-12 mb-0"),
                    Column("focus_area", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
            ),
            FormActions(
                Submit("save", "Create a SubProject"),
                HTML('<a class="btn btn-danger" href="/projects/subprojects/list">Cancel</a>'),
            ),
        )

    def save(self, commit=True):
        instance = super(SubProjectForm, self).save(commit=False)
        instance.save()
        self.save_m2m()
        return instance
