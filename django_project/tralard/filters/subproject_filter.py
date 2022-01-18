from django_filters import rest_framework as filters

from tralard.models import SubProject


class SubprojectFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )
    project__slug = filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = SubProject
        fields = ["name", "program__project__slug"]
