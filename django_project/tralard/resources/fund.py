# coding=utf-8
"""
Fund model resource class definitions for tralard app.
"""

from import_export import resources

from tralard.models.fund import (
    Fund,
    Disbursement,
    Expenditure,
    FundVersion
)


class FundResource(resources.ModelResource):
    class Meta:
        model = Fund
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "slug",
            "amount_currency",
            "amount",
            "approved",
            "approval_status",
            "approval_status_comment",
            "balance_currency",
            "balance",
            "variation_currency",
            "variation",
            "funding_date",
            "currency",
            "sub_project",
            "requested_by",
            "approved_by",
            "approved_date",
            "created",
        )


class FundVersionResource(resources.ModelResource):
    class Meta:
        model = FundVersion
        
        fields = (
            "amount",
            "approved",
            "approval_status",
            "approval_status_comment",
            "balance",
            "funding_date",
            "currency",
            "requested_by",
            "approved_by",
            "approved_date",
        )


class DisbursementResource(resources.ModelResource):
    class Meta:
        model = Disbursement
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "slug",
            "amount_currency",
            "amount",
            "balance_currency",
            "balance",
            "disbursement_date",
            "currency",
            "fund",
            "created",
        )


class ExpenditureResource(resources.ModelResource):
    class Meta:
        model = Expenditure
        widgets = {
            "created": {"format": "%d.%m.%Y"},
        }
        fields = (
            "id",
            "slug",
            "amount",
            "currency",
            "expenditure_date",
            "disbursment",
            "created",
        )
