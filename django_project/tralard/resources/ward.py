# coding=utf-8
"""
Ward model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.ward import Ward


class WardResource(resources.ModelResource):
    class Meta:
        model = Ward
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "name",
            "created",
            "location",
            "district",
        )
