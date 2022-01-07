# coding=utf-8
"""
Sub Project model definitions for tralard app.
"""
import logging

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from tralard.models.fund import Fund
from tralard.models.beneficiary import Beneficiary

from tralard.utils import unique_slugify


from tinymce import HTMLField

logger = logging.getLogger(__name__)


class Indicator(models.Model):
    """
    Sub Project Indicator Representative.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    name = models.CharField(
        _("Name"),
        max_length=200,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.name.lower()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

class SubProject(models.Model):
    """
    Sub Project definition.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    name = models.CharField(
        help_text=_('Name of this Sub Project.'),
        max_length=255,
        unique=True
    )
    size = models.CharField(
        help_text=_(
            'Size (number of Hectors, SquareMeters, Products etc,).'),
        max_length=255,
        blank=True,
        null=True
    )
    supervisor = models.ForeignKey(
        'tralard.representative',
        help_text=_(
            'Sub Project Supervisor. '
            'This name will be used on trainings and any other references. '),
        on_delete=models.SET_NULL,
        blank=True,
        null=True  # This is needed to populate existing database.
    )
    project = models.ForeignKey(
        'tralard.Project', 
        default='',
        on_delete=models.CASCADE,
    )
    indicators = models.ManyToManyField(
        Indicator,
        related_name='subproject_indicators',
        blank=True,
        # null=True, null has no effect on ManyToManyField.
    )
    subproject_managers = models.ManyToManyField(
        'tralard.Representative',
        related_name='subproject_managers',
        blank=True,
        # null=True, null has no effect on ManyToManyField.
        help_text=_(
            'Managers of all trainings and project activities in this Sub project. '
            'They will be allowed to create or delete subproject data.')
    )
    approved = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    image_file = models.ImageField(
        help_text=_(
            'A banner image for this Sub Project. Most browsers support dragging '
            'the image directly on to the "Choose File" button above. The '
            'ideal size for your image is 512 x 512 pixels.'),
        upload_to='images/projects',
        blank=True
    )
    description = models.TextField(
        help_text=_(
            'A detailed summary of the Sub Project. Rich text edditing is supported.'),
        max_length=2000,
        blank=True,
        null=True
    )
    focus_area = HTMLField(
        help_text=_(
            'Please describe the focus areas of the sub project.'
            '(if any). Rich text editing is supported'),
        max_length=10000,
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    # def get_absolute_url(self):
    #     """Return URL to project detail page
    #     :return: URL
    #     :rtype: str
        # """
        # return reverse('project-detail', kwargs={'pk': self.pk})
    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

    @property 
    def get_related_project(self):
        return self.project.name

    @property 
    def fund_utilization_percent(self):
        project_id = self.project.id
        fund_obj = Fund.objects.get(id=self.id)
        initial_fund = fund_obj.amount
        balance = fund_obj.balance
        fund_utilization_percent = ( balance / initial_fund ) * 100
        return fund_utilization_percent

    @property
    def count_beneficiaries(self):
        beneficiary_count_queryset = Beneficiary.objects.filter(
            sub_project__slug=self.slug
            ).count()
        return beneficiary_count_queryset

    @property
    def count_indicators(self):
        subproject_indicators = Indicator.objects.filter(
            subproject_indicators__slug=self.slug
        ).count()
        return subproject_indicators
