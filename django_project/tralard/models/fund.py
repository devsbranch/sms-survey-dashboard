# coding=utf-8
"""
Fund model definitions for tralard app.
"""
import logging

from django.db import models
from django.db.models.aggregates import Sum
from django.utils.translation import gettext_lazy as _
from tralard.utils import check_requested_deduction_against_balance, compute_total_amount, get_balance

from djmoney.models.fields import MoneyField

from tralard.models.project import Project

logger = logging.getLogger(__name__)


class ApprovedFundManager(models.Manager):
    """Custom manager that shows pproved project funds."""
    def get_queryset(self):
        return super(
            ApprovedFundManager, self
        ).get_queryset().filter(
            approved=True,)


class UnapprovedFundManager(models.Manager):
    """Custom fund manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            UnapprovedFundManager, self).get_queryset().filter(
                approved=False)


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
    balance = MoneyField(
        _("Balance"),
        max_digits=14,
        decimal_places=2,
        default=0.0
    )
    variation = MoneyField(
        _("Variation"),
        max_digits=14,
        decimal_places=2,
        null=True,
        default_currency="ZMW",
        help_text="Variation if any.",
        default=0.0
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
    objects = models.Manager()
    approved_objects = ApprovedFundManager()
    unapproved_objects = UnapprovedFundManager()

    # noinspecti
    class Meta:
        verbose_name = _('Fund')
        verbose_name_plural = _('Funds')

    def __str__(self):
        return f"Amount {self.amount}, Project {self.project}."


    def save(self, *args, **kwargs):
        """
        Override save method to calculate the balance.
        """
        if self.amount is not None:
            total_disburesment = compute_total_amount(FundDisbursed, self.pk, "disbursement")
            self.balance = get_balance(self.amount, total_disburesment)
        super().save(*args, **kwargs)


class FundDisbursed(models.Model):
    """
    Project Fund disbursement definition.
    """
    amount = MoneyField(
        _("Amount Disbursed"),
        max_digits=14,
        decimal_places=2,
        null=True,
        default_currency="ZMW",
        help_text="Amount disbursed for the project.",
    )
    balance = MoneyField(
        _("Balance"),
        max_digits=14,
        decimal_places=2,
        default=0.0
    )
    disbursement_date = models.DateField(
        _("Disbursement Date"),
        null=True,
        blank=True,
        help_text="The date the project was disbursed.",
    )
    currency = models.CharField(
        help_text=_('Currency for the project Fund.'),
        choices=Fund.CURRENCY_CHOICES,
        max_length=10,
        blank=True,
        null=True
    )    
    fund = models.ForeignKey(
        Fund,
        on_delete=models.PROTECT,
    )    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Disbursed Fund")
        verbose_name_plural = _("Disbursed Funds")

    def __str__(self):
        return f"Amount {self.amount}, Fund {self.fund}."
    
    def save(self, *args, **kwargs):
        """
        Override save method to calculate the balance.
        """
        if self.amount is not None:
            self.amount = check_requested_deduction_against_balance(
                self.fund.balance, 
                self.amount, 
                'Disbursement', 
                'Fund'
                )
            total_disbursment = compute_total_amount(FundExpenditure, self.pk, "expenditure")
            self.balance = get_balance(self.amount, total_disbursment)
        super().save(*args, **kwargs)


class FundExpenditure(models.Model):
    """
    Funds Expenditure definition.
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
        _("Amount"),
        max_digits=14,
        decimal_places=2,
        null=True,
        default_currency="ZMW",
        help_text="Amount spent on from disbused funds.",
    )
    expenditure_date = models.DateField(
        _("Expenditure Date"),
        null=True,
        blank=True,
        help_text="The date the amount was spent.",
    )
    currency = models.CharField(
        help_text=_('Currency for the Expenditure.'),
        choices=CURRENCY_CHOICES,
        max_length=10,
        blank=True,
        null=True
    )
    disbursment = models.ForeignKey(
        FundDisbursed,
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Expenditure")
        verbose_name_plural = _("Expenditures")

    def __str__(self):
        return f"Amount {self.amount}, Disbursement {self.disbursment}."

    def save(self, *args, **kwargs):
        self.amount = check_requested_deduction_against_balance(
            self.disbursment.balance,
            self.amount,
            'Expenditure',
            'Disbursed'
            )
        super().save(*args, **kwargs)