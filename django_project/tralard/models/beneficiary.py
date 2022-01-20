# coding=utf-8
"""
Beneficiary model definitions for tralard app.
"""
import logging

from django.db.models import Sum
from django.utils.text import slugify
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from dj_beneficiary.models import AbstractOrganizationBeneficiary
from tralard.models.ward import Ward
from tralard.utils import unique_slugify

logger = logging.getLogger(__name__)

class BeneficiaryManager(models.Manager):
    """Custom manager that aggregates beneficiary overview."""
    def get_total_females(self):
        return super(
            BeneficiaryManager, self
        ).get_queryset().aggregate(
            Sum('total_females'))['total_females__sum']

    def get_total_males(self):
        return super(
            BeneficiaryManager, self
        ).get_queryset().aggregate(
            Sum('total_males'))['total_males__sum']

    def get_total_hhs(self):
        return super(
            BeneficiaryManager, self
        ).get_queryset().aggregate(
            Sum('total_hhs'))['total_hhs__sum']

    def get_female_hhs(self):
        return super(
            BeneficiaryManager, self
        ).get_queryset().aggregate(
            Sum('female_hhs'))['female_hhs__sum']
        
class Beneficiary(AbstractOrganizationBeneficiary):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    location = models.PointField(
        _("Location"), geography=True, blank=True, null=True, srid=4326
    )
    ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
    )
    sub_project = models.ForeignKey(
        "tralard.subproject",
        on_delete=models.CASCADE,
    )
    
    objects = models.Manager()
    custom_objects = BeneficiaryManager()

    class Meta:
        abstract = False
        verbose_name = "Beneficiary Organization"
        verbose_name_plural = "Beneficiary Organizations"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)
