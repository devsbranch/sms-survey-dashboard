# coding=utf-8
"""
Province model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.province import Province


class ProvinceResource(resources.ModelResource):
    class Meta:
        model = Province
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id", 
            "name", 
            "location"
        )
