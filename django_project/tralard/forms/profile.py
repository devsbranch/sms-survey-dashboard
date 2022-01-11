from django.contrib.gis import forms

from django.forms import ModelForm, widgets

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    HTML,
    Fieldset,
    Submit,
    Row,
    Column,
)
from crispy_forms.bootstrap import FormActions

from tralard.models.profile import Profile

class ProfileForm(ModelForm):
    class Meta:

        model = Profile
        exclude = ["id", "slug", "user"]
        widgets = {
            'birth_date': widgets.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'type':'date'}),
            'about_me': forms.TextInput(attrs={'size': 500, 'title': 'Training Scheddule Notes',  'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
                Row(
                    Column("birth_date", css_class="form-group col-md-12 mb-0"),
                    Column("gender", css_class="form-group col-md-12 mb-0"),
                    Column("about_me", css_class="form-group col-md-12 mb-0"),
                    Column("education_level", css_class="form-group col-md-12 mb-0"),
                    Column("cell", css_class="form-group col-md-12 mb-6"),
                    Column("postal_code", css_class="form-group col-lg-12"),
                    Column("district", css_class="form-group col-lg-12"),
                    Column("profile_photo", css_class="form-group col-md-12 mb-0"),
                    Column("address", css_class="form-group col-lg-12"),
                ),
            FormActions(
                HTML("<button class='btn' type='submit' style='background: #21546d; color: white; font-size: 14px;'>Update Profile Details</button>"),
            ),
        )
        
    def save(self, commit=True):
        instance = super(ProfileForm, self).save(commit=False)
        instance.save()
        return instance
