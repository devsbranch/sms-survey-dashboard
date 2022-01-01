# coding=utf-8
"""
District model definitions for tralard app.
"""
import logging

from django.utils.text import slugify
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from tralard.utils import unique_slugify

from tralard.models.province import Province

from dj_beneficiary.models import AbstractLocation


logger = logging.getLogger(__name__)


class District(AbstractLocation):
    """
    District Locatoin Model.
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
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
    )
    
    class Meta:
        abstract = False
        verbose_name = "District"
        verbose_name_plural = "Districts"


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

District._meta.get_field('name').verbose_name = 'District name'
District._meta.get_field('name').help_text = 'The name of the district.'