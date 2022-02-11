# coding=utf-8
"""
SubProject model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.sub_project import (
    SubProject
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
            "managers",
            "approved",
            "status",
            "description",
            "focus_area",
        )
