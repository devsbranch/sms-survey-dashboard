# coding=utf-8
"""
Beneficiary model definitions for tralard app.
"""
import logging

from django.utils.text import slugify
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from tralard.models.ward import Ward

from tralard.utils import unique_slugify

from dj_beneficiary.models import AbstractOrganizationBeneficiary

logger = logging.getLogger(__name__)


class Beneficiary(AbstractOrganizationBeneficiary):
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    location = models.PointField(
        _("Location"),
        geography=True,
        blank=True,
        null=True,
        srid=4326
    )
    ward = models.ForeignKey(
        Ward, 
        on_delete=models.CASCADE,
    )
    sub_project = models.ForeignKey(
        'tralard.subproject',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = False
        verbose_name = "Beneficiary Organization"
        verbose_name_plural = "Beneficiary Organizations"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)