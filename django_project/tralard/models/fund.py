# coding=utf-8
"""
Fund model definitions for tralard app.
"""
from datetime import datetime
import logging

from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db.models.aggregates import Sum
from django.utils.translation import gettext_lazy as _
from tralard.utils import (
    get_balance,
    unique_slugify,
    compute_total_amount, 
    check_requested_deduction_against_balance
)

from djmoney.models.fields import MoneyField
from djmoney.money import Money


logger = logging.getLogger(__name__)

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

class FundCountManager(models.Manager):
    """ Computes total funds spent in current year """
    def get_total_funds_in_year(self):   
        current_year = datetime.now().year
        year_labels = list(set(list()))
        year_data = list(set(list()))

        for i in range(5):
            year_labels.append(current_year - i)
            year_data.append(
                int(self.get_queryset().filter(funding_date__year__gte=current_year - i, funding_date__year__lte=current_year - i
                ).aggregate(
                    total_funds=Sum('amount')
                )['total_funds'] or 0)
            )     
   
        
        return {
            'year_labels': year_labels,
            'total_funds': year_data            
        }

class Fund(models.Model):
    """
    Project Fund definition.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    amount = MoneyField(
        _("Amount Approved"),
        max_digits=14,
        decimal_places=2,
        default_currency=ZMK,
        help_text="Amount approved for the project.",
        default=Money('0.0', ZMK)
    )
    approved = models.BooleanField(
        help_text=_('Whether this project fund has been approved for use yet.'),
        default=False
    )
    balance = MoneyField(
        _("Balance"),
        max_digits=14,
        decimal_places=2,
        default=Money(0.0, 'ZMK')
    )
    variation = MoneyField(
        _("Variation"),
        max_digits=14,
        decimal_places=2,
        null=True,
        default_currency=ZMK,
        help_text="Variation if any.",
        default=Money('0.0', ZMK)
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
        default=ZMK,
    )
    sub_project = models.ForeignKey(
        'tralard.SubProject',
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    approved_objects = ApprovedFundManager()
    unapproved_objects = UnapprovedFundManager()
    count_objects = FundCountManager()

    # noinspecti
    class Meta:
        verbose_name = _('Fund')
        verbose_name_plural = _('Funds')

    class Meta:
        verbose_name = _('Fund')
        verbose_name_plural = _('Funds')

    def __str__(self):
        return f"Amount: {self.amount}, SubProject: {self.sub_project}, Program: {self.sub_project.project.program.name}."


    def save(self, *args, **kwargs):
        """
        Override save method to calculate the balance.
        """
        if not self.slug:
            self.slug = unique_slugify(self, 
            slugify(f"{self.sub_project.project.slug} \
                fund amount \
                    {self.amount}"
                    )
                )
            
        if self.amount is not None:
            total_disburesment = compute_total_amount(Disbursement, self.pk, "disbursement")
            self.balance = get_balance(self.amount, total_disburesment)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        """Return URL to project detail page
        :return: URL
        :rtype: str
        """
        return reverse_lazy('tralard:project-detail', 
            kwargs={
                'program_slug': self.sub_project.project.program.slug, 
                'project_slug': self.sub_project.project.slug
                }
            )
    @property
    def total_disbursed_funds(self):
        total_disbursed_funds_queryset = Disbursement.objects.filter(
            fund__id=self.pk
            )
        return total_disbursed_funds_queryset

    @property
    def get_total_disbursements(self):
        """Computes total Expenses related to this Disbursement."""
        related_funds_sum_qs = Disbursement.objects.filter(
            fund__id=self.pk
        ).aggregate(Sum('amount'))

        amount_value = related_funds_sum_qs['amount__sum']
        return amount_value
          
class Disbursement(models.Model):
    """
    Project Fund disbursement definition.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    amount = MoneyField(
        _("Amount Disbursed"),
        max_digits=14,
        decimal_places=2,
        default_currency=ZMK,
        help_text="Amount disbursed for the project.",
        default=Money('0.0', ZMK)
    )
    balance = MoneyField(
        _("Balance"),
        max_digits=14,
        decimal_places=2,
        default=Money('0.0', ZMK)
    )
    disbursement_date = models.DateField(
        _("Disbursement Date"),
        null=True,
        blank=True,
        help_text="The date the project was disbursed.",
    )
    currency = models.CharField(
        help_text=_('Currency for the project Fund.'),
        choices=CURRENCY_CHOICES,
        max_length=10,
        default=ZMK,
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
        return f"Amount: {self.amount}, Fund: {self.fund}. Project: {self.fund.sub_project.project.name}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to calculate the balance.
        """
        if not self.slug:
            self.slug = unique_slugify(self, slugify(
                f'{self.fund.slug} \
                    disbursement amount \
                        {self.amount}'
                        )
                    )
        if self.amount is not None:
            self.amount = check_requested_deduction_against_balance(
                self.fund.balance, 
                self.amount, 
                'Disbursement', 
                'Fund'
                )
            total_disbursment = compute_total_amount(Expenditure, self.pk, "expenditure")
            self.balance = get_balance(self.amount, total_disbursment)
        super().save(*args, **kwargs)

    @property
    def total_disbursed_expenses(self):
        total_disbursed_expenses_queryset = Expenditure.objects.filter(
            disbursment__id=self.pk
            )
        return total_disbursed_expenses_queryset

    @property
    def get_total_disbursed_expenses(self):
        """Computes total Expenses related to this Disbursement."""
        related_funds_sum_qs = Expenditure.objects.filter(
            disbursment__id=self.pk
        ).aggregate(Sum('amount'))

        amount_value = related_funds_sum_qs['amount__sum']
        return amount_value

class Expenditure(models.Model):
    """
    Funds Expenditure definition.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    amount = MoneyField(
        _("Amount"),
        max_digits=14,
        decimal_places=2,
        default_currency=ZMK,
        help_text="Amount spent on from disbused funds.",
        default=Money('0.0', ZMK)
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
        default=ZMK,
    )
    disbursment = models.ForeignKey(
        Disbursement,
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Expenditure")
        verbose_name_plural = _("Expenditures")

    def __str__(self):
        return f"Amount {self.amount}, Disbursement {self.disbursment}. Project: {self.disbursment.fund.sub_project.project.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(
                self, slugify(
                    f'{self.disbursment.slug} \
                        expenditure amount {self.amount}'
                    )
                )
        self.amount = check_requested_deduction_against_balance(
            self.disbursment.balance,
            self.amount,
            'Expenditure',
            'Disbursed'
            )
        super().save(*args, **kwargs)
        


