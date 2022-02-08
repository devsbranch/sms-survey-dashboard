import django_filters

from tralard.models import Project


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    program__slug = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = Project
        fields = ["name", "program"]
