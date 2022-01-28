# coding=utf-8
"""
Beneficiary model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.beneficiary import Beneficiary


class BeneficiaryResource(resources.ModelResource):
    class Meta:
        model = Beneficiary
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "name",
            "org_type",
            "total_beneficiaries",
            "total_females",
            "total_males",
            "total_hhs",
            "female_hhs",
            "below_sixteen",
            "sixteen_to_thirty",
            "thirty_to_fourty_five",
            "above_fourty_five",
            "description",
            "email",
            "cell",
            "registered_date",
            "created",
            "location",
            "ward",
            "sub_project",
        )
