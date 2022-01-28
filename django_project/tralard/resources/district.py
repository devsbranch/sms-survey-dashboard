# coding=utf-8
"""
District model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.district import District


class DistrictResource(resources.ModelResource):
    class Meta:
        model = District
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "name",
            "created",
            "location",
            "province",
        )
