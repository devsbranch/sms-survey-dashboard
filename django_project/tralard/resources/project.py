# coding=utf-8
"""
Project model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.project import Project


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
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
            "program",
            "project_representative",
            "project_managers",
            "project_funders",
            "training_managers",
            "certification_managers",
            "precis",
            "focus_area",
        )
