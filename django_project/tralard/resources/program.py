# coding=utf-8
"""
Program model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.program import Program


class ProgramResource(resources.ModelResource):
    class Meta:
        model = Program
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "name",
            "approved",
            "started",
            "program_representative",
            "description",
        )
