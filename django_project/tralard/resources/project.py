# coding=utf-8
"""
Program model resource class definitions for tralard app.
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
            "started",
            "project_representative",
            "description",
        )
