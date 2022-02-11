# coding=utf-8
"""
SubComponent model definitions for tralard app.
"""
import os
import logging

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from tralard.models.fund import Fund
from tralard.utils import unique_slugify
# (TODO:Alison) take the get_related_sub_project method to utilities or model managers.
# not very safe (circular import issue candidate) 
# except that we are referencing to SubComponent under subproject via string reference 
# and not by imoprt - so its safe this way
from tralard.models.sub_project import SubProject
from tralard.models.beneficiary import Beneficiary
from tralard.constants import PROJECT_STATUS_CHOICES, MODEL_FIELD_CHOICES

from tinymce import HTMLField

User = get_user_model()
logger = logging.getLogger(__name__)


class ApprovedSubComponentManager(models.Manager):
    """Custom manager that shows approved subcomponents."""

    def get_queryset(self):
        return super(
            ApprovedSubComponentManager, self
        ).get_queryset().filter(
            approved=True, )


class UnapprovedSubComponentManager(models.Manager):
    """Custom subcomponent manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            UnapprovedSubComponentManager, self).get_queryset().filter(
            approved=False)

class SubComponent(models.Model):
    """
    SubComponent definition.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )

    name = models.CharField(
        help_text=_('Name of this subcomponent.'),
        max_length=255,
        unique=True
    )
    indicators = models.ManyToManyField(
        "tralard.Indicator",
        related_name="indicator_related_subcomponents",
        blank=True,
        # null=True, null has no effect on ManyToManyField.
    )
    approved = models.BooleanField(
        help_text=_('Whether this subcomponent has been approved yet.'),
        default=False,
        null=True
    )
    has_funding = models.BooleanField(
        help_text=_('Whether this subcomponent has an active funding.'),
        default=False,
        null=True
    )
    status = models.CharField(
        _("SubComponent Status"),
        max_length=50,
        choices=PROJECT_STATUS_CHOICES,
        null=True,
        blank=True,
    )
    description = models.CharField(
        help_text=_('A short description for the subcomponent'),
        max_length=500,
        blank=True,
        null=True
    )
    project = models.ForeignKey(
        'tralard.project',
        default='',
        on_delete=models.CASCADE,
    )
    image_file = models.ImageField(
        help_text=_(
            'A banner image for this subcomponent. Most browsers support dragging '
            'the image directly on to the "Choose File" button above. The '
            'ideal size for your image is 512 x 512 pixels.'),
        upload_to='images/subcomponents',
        blank=True
    )
    precis = HTMLField(
        help_text=_(
            'A detailed summary of the subcomponent. Rich text edditing is supported.'),
        blank=True,
        null=True
    )

    focus_area = HTMLField(
        help_text=_(
            'Please describe the focus areas of the subcomponent.'
            '(if any). Rich text editing is supported'),
        blank=True,
        null=True
    )

    objects = models.Manager()
    approved_objects = ApprovedSubComponentManager()
    unapproved_objects = UnapprovedSubComponentManager()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to subcomponent detail page
        :return: URL
        :rtype: str
        """
        return reverse_lazy('tralard:subcomponent-detail',
                    kwargs={
                        'project_slug': self.project.slug,
                        'subcomponent_slug': self.slug
                    }
                )

    @property
    def get_related_sub_projects(self):
        sub_projects_queryset = SubProject.objects.filter(
            subcomponent__slug=self.slug
        )
        return sub_projects_queryset

    @property
    def count_sub_projects(self):
        sub_projects_count_queryset = SubProject.objects.filter(
            subcomponent__slug=self.slug
        ).count()
        return sub_projects_count_queryset

    @property
    def get_total_sub_project_fund(self):
        total_sub_project_fund = Fund.objects.filter(
            sub_project__subcomponent__slug=self.slug
        ).aggregate(Sum('amount'))
        amount_value = total_sub_project_fund["amount__sum"]
        return amount_value

    @property
    def count_beneficiaries(self):
        beneficiary_count_queryset = Beneficiary.objects.filter(
            sub_project__subcomponent__slug=self.slug
        ).count()
        return beneficiary_count_queryset

    @property
    def get_total_subcomponent_fund(self):
        """Computes total funds related to this project."""
        related_funds_sum_qs = Fund.objects.filter(
            sub_project__subcomponent__slug=self.slug
        ).aggregate(Sum('amount'))

        amount_value = related_funds_sum_qs['amount__sum']
        return amount_value

    @property
    def get_total_fund_balance(self):
        """Computes total funds balance related to this project."""
        related_funds_balance_sum_qs = Fund.objects.filter(
            sub_project__subcomponent__slug=self.slug
        ).aggregate(Sum('balance'))

        amount_value = related_funds_balance_sum_qs['balance__sum']
        return amount_value

    @property
    def count_approved_sub_projects(self):
        """Returns approved sub-projects of this project."""
        sub_projects_queryset = SubProject.objects.filter(
            subcomponent__slug=self.slug,
            approved=True
        ).count()
        return sub_projects_queryset

    @property
    def count_indicators(self):
        indicator_related_subcomponents = Indicator.objects.filter(
            indicator_related_subcomponents__slug=self.slug
        ).count()
        return indicator_related_subcomponents

    @property
    def get_total_used_funds(self):
        """Computes total funds used related to this subcomponent."""
        total_subcomponent_funds = self.get_total_subcomponent_fund
        total_subcomponent_funds_balance = self.get_total_fund_balance
        try:
            total_subcomponent_funds_used = total_subcomponent_funds - total_subcomponent_funds_balance
        except:
            total_subcomponent_funds_used = 0
        return total_subcomponent_funds_used

    @property
    def get_total_used_funds_percent(self):
        """Computes total funds utilized as a percent related to this subcomponent."""
        total_subcomponent_funds = self.get_total_subcomponent_fund
        total_subcomponent_funds_utilized_percent = (self.get_total_used_funds / total_subcomponent_funds) * 100
        return round(total_subcomponent_funds_utilized_percent)

    @property
    def logo_url(self):
        if self.image_file:
            return self.image_file.url
        return os.path.join(settings.STATIC_URL, "assets/images/logos/logo.png")


class Indicator(models.Model):
    """
    Sub Project Indicator Representative.
    """
       
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True,
    )
    name = models.CharField(
        _("Name"),
        max_length=200,
    )

    def __str__(self):
        return self.name.lower()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

class IndicatorTarget(models.Model):
    """
    Stores a single Indicator target entry, related to model 'Indicator'.
    """
    unit_of_measure = models.ForeignKey(
        "tralard.IndicatorUnitOfMeasure", 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True,
        help_text="A brief description of this indicator target.",
    )
    baseline_value = models.CharField(
        _("Baseline Value"),
        max_length=200,
        null=True,
        blank=True,
        help_text="A baseline is data or measurement that is collected prior to the implementation of the project.",
    )
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description[:75]}| {self.unit_of_measure} Target"


class IndicatorTargetValue(models.Model):
    year =  models.DateField(_('Target Year'))
    target_value =  models.CharField(
        _('Target Value'),
        max_length=200,
        default=0
    )
    indicator_target =  models.ForeignKey(
        IndicatorTarget,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.indicator_target.description} Target for: {self.year.year}"


class IndicatorUnitOfMeasure(models.Model):
    unit_of_measure = models.CharField(
        _("Unit of Measure"), max_length=200,
        null=True,
        blank=True
    )
    data_source = models.CharField(
        _("Source of data"), 
        max_length=200,
        choices=MODEL_FIELD_CHOICES
    )

    def __str__(self):
        return self.unit_of_measure
    
    def get_actual_data(self, indicator_obj):
        """
        This method returns data to be used in the indicator report. This data
        returned is a number which is a Sum total of the field data for all Sub Projects
        under the given Indicator.
        """

        sub_project_filter = {"sub_project__subcomponent__indicators": indicator_obj}
        
        total = 0

        if self.data_source == "size":
            filter_by = {"subcomponent__indicators": indicator_obj}
            try:
                total = float(SubProject.objects.filter(**filter_by).aggregate(Sum('size'))['size__sum'])
            except TypeError:
                total = 0

        elif self.data_source == "total_beneficiaries":
            total = Beneficiary.custom_objects.get_total_beneficiaries(sub_project_filter)

        elif self.data_source == "total_females":
            total = Beneficiary.custom_objects.get_total_females(sub_project_filter)
        
        elif self.data_source == "total_males":
            total = Beneficiary.custom_objects.get_total_males(sub_project_filter)
        
        elif self.data_source == "total_hhs":
            total = Beneficiary.custom_objects.get_total_hhs(sub_project_filter)
        
        elif self.data_source == "female_hhs":
            total = Beneficiary.custom_objects.get_female_hhs(sub_project_filter)
        elif self.data_source == "beneficiary_orgs":
            total = Beneficiary.objects.filter(**sub_project_filter).count()

        return total

class Feedback(models.Model):
    """
    SubComponent Feedback.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    title = models.CharField(
        _("Title"),
        max_length=200,
    )
    date = models.DateField(
        _("Create Date"),
        auto_now_add=False,
        null=True,
        blank=True
    )
    subcomponent = models.ForeignKey(
        SubComponent,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    moderator = models.ForeignKey(
        User,
        related_name='feedback_moderator',
        help_text=_(
            'Feedback Moderator. '
            'This name will be used on subcomponent feedback and any other references. '),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} subcomponent: {self.subcomponent.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)
