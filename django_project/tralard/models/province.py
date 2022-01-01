# coding=utf-8
"""
Province model definitions for tralard app.
"""
import logging

from django.utils.text import slugify
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from tralard.utils import unique_slugify

from dj_beneficiary.models import AbstractLocation


logger = logging.getLogger(__name__)


class Province(AbstractLocation):
    """
    Province Locatoin Model.
    """
    slug = models.SlugField(
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
    class Meta:
        abstract = False
        verbose_name = "Province"
        verbose_name_plural = "Provinces"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

Province._meta.get_field('name').verbose_name = 'Province name'
Province._meta.get_field('name').help_text = 'The name of the province.'
