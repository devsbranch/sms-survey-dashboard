# coding=utf-8
"""
Project model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.subcomponent import (
    SubComponent, 
    Indicator, 
    IndicatorTarget, 
    IndicatorTargetValue
)


class SubComponentResource(resources.ModelResource):
    class Meta:
        model = SubComponent
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "name",
            "approved",
            "indicators",
            "has_funding",
            "status",
            "description",
            "project",
            "precis",
            "focus_area",
        )



class IndicatorResource(resources.ModelResource):
    class Meta:
        model = Indicator
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = ("id", "name")


class IndicatorTargetResource(resources.ModelResource):
    class Meta:
        model = IndicatorTarget
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id", 
            "unit_of_measure", 
            "description", 
            "baseline_value", 
            "indicator"
        )


class IndicatorTargetValueResource(resources.ModelResource):
    class Meta:
        model = IndicatorTargetValue
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id", 
            "year", 
            "target_value", 
            "actual_value", 
            "indicator_target"
        )
