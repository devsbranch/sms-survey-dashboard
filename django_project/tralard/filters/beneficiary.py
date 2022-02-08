import django_filters

from tralard.models import Beneficiary


class BeneficiaryFilter(django_filters.FilterSet):
    class Meta:
        model = Beneficiary
        fields = ["ward", "sub_project"]
