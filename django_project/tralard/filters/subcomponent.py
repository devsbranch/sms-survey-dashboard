import django_filters

from tralard.models import SubComponent


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    project__slug = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = SubComponent
        fields = ["name", "project"]
