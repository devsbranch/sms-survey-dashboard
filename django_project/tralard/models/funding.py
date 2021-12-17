from django.db import models
from django.utils.translation import gettext_lazy as _

from djmoney.models.fields import MoneyField


class Funding(models.Model):
    """
    Project Funding definition.
    """

    amount_approved = MoneyField(
        _("Amount Approved"),
        max_digits=14,
        decimal_places=2,
        null=True,
        default_currency="ZMW",
        help_text="Amount approved for the project.",
    )
    disbursed_amount_to_date = MoneyField(
        _("Disbursed amount to date"),
        max_digits=14,
        decimal_places=2,
        null=True,
        default_currency="ZMW",
    )
    expenditure = MoneyField(
        _("Expenditure"),
        max_digits=14,
        decimal_places=2,
        null=True,
        default_currency="ZMW",
        help_text="Amount spent on the project to date.",
    )
    funding_date = models.DateField(
        _("Funding Date"),
        null=True,
        blank=True,
        help_text="The date the project was funded.",
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount_approved} approved and {self.expenditure} has been spent."
