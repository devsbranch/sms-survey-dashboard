# coding=utf-8
"""
SubProject model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.sub_project import (
    Indicator,
    SubProject,
    IndicatorTarget,
    IndicatorTargetValue,
)


class SubProjectResource(resources.ModelResource):
    class Meta:
        model = SubProject
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "name",
            "size",
            "ward",
            "representative",
            "project",
            "indicators",
            "managers",
            "approved",
            "status",
            "description",
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
