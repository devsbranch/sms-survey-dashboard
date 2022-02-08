import django_filters

from tralard.models import Fund


class FundFilter(django_filters.FilterSet):
    class Meta:
        model = Fund
        fields = ["approved", "sub_project", "funding_date"]
