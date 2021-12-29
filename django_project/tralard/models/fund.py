# coding=utf-8
"""
Fund model definitions for tralard app.
"""
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from djmoney.models.fields import MoneyField

from tralard.models.project import Project

logger = logging.getLogger(__name__)


class Fund(models.Model):
    """
    Project Fund definition.
    """
    ZMK = 'ZMK'
    USD = 'USD'
    GBP = 'GBP'
    EU = 'EU'
    CURRENCY_CHOICES = [
        (ZMK, 'ZMK'), 
        (USD, 'USD'),
        (GBP, 'GBP'),
        (EU, 'EU')
    ]

    amount = MoneyField(
        _("Amount Approved"),
        max_digits=14,
        decimal_places=2,
        null=True,
        default_currency="ZMW",
        help_text="Amount approved for the project.",
    )
    approved = models.BooleanField(
        help_text=_('Whether this project fund has been approved for use yet.'),
        default=False
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
    variation = MoneyField(
        _("Variation"),
        max_digits=14,
        decimal_places=2,
        null=True,
        default_currency="ZMW",
        help_text="Variation if any.",
    )
    funding_date = models.DateField(
        _("Funding Date"),
        null=True,
        blank=True,
        help_text="The date the project was funded.",
    )
    currency = models.CharField(
        help_text=_('Currency for the project Fund.'),
        choices=CURRENCY_CHOICES,
        max_length=10,
        blank=True,
        null=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Amount {self.amount}, Project {self.project}."
