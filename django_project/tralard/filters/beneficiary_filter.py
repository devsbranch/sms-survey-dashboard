from django_filters import rest_framework as filters

from tralard.models import Beneficiary


class BeneficiaryFilter(filters.FilterSet):
    class Meta:
        model = Beneficiary
