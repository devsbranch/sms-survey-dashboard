# coding=utf-8
"""
Province model definitions for tralard app.
"""
import logging

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from dj_beneficiary.models import AbstractLocation


logger = logging.getLogger(__name__)


class Province(AbstractLocation):
    """
    Province Locatoin Model.
    """
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

Province._meta.get_field('name').verbose_name = 'Province name'
Province._meta.get_field('name').help_text = 'The name of the province.'
