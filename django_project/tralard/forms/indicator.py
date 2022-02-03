from attr import fields
from django.forms import ModelForm, widgets

from tralard.models import Indicator, IndicatorTarget, IndicatorTargetValue, IndicatorUnitOfMeasure


class IndicatorForm(ModelForm):
    class Meta:
        model = Indicator
        exclude = ("slug",)
        

class IndicatorTargetForm(ModelForm):
    class Meta:
        model = IndicatorTarget
        fields = "__all__"


class IndicatorTargetValueForm(ModelForm):
    class Meta:
        model = IndicatorTargetValue
        fields = "__all__"

        widgets = {
            "year": widgets.DateInput(
                format=("%m/%d/%Y"),
                attrs={
                    "type": "date",
                },
            )
        }


class IndicatorUnitOfMeasureForm(ModelForm):
    class Meta:
        model = IndicatorUnitOfMeasure
        fields = "__all__"
