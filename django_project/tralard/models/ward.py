# coding=utf-8
"""
Ward model definitions for tralard app.
"""
import logging

from django.utils.text import slugify
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from tralard.models.district import District

from tralard.utils import unique_slugify

from dj_beneficiary.models import AbstractLocation


logger = logging.getLogger(__name__)


class Ward(AbstractLocation):
    """
    District Locatoin Model.
    """
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
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    
    class Meta:
        abstract = False
        verbose_name = "Ward"
        verbose_name_plural = "Wards"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

Ward._meta.get_field('name').verbose_name = 'Ward name'
Ward._meta.get_field('name').help_text = 'The name of the ward.'
