from django.db import models
from djmoney.models.fields import MoneyField


class Funding(models.Model):
    """
    Project Funding definition.
    """

    amount_approved = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="ZMW",
        help_text="Amount approved for the project.",
    )
    disbursed_amount_to_date = MoneyField(
        max_digits=14, decimal_places=2, default_currency="ZMW"
    )
    expenditure = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="ZMW",
        help_text="Amount spent on the project to date.",
    )
    funding_date = models.DateField(
        null=True, blank=True, help_text="The date the project was funded."
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount_approved} approved and {self.expenditure} has been spent."
