from django_filters import rest_framework as filters

from tralard.models import Project


class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )
    program__slug = filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = Project
        fields = ["name", "program"]
