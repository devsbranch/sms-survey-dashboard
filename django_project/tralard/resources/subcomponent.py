# coding=utf-8
"""
Project model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.subcomponent import SubComponent


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
            "has_funding",
            "status",
            "description",
            "project",
            "precis",
            "focus_area",
        )
