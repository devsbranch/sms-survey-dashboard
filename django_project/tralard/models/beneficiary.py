# coding=utf-8
"""
Beneficiary model definitions for tralard app.
"""
import logging

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from tralard.models.sub_project import SubProject
from tralard.models.ward import Ward

from dj_beneficiary.models import AbstractOrganizationBeneficiary

logger = logging.getLogger(__name__)


class Beneficiary(AbstractOrganizationBeneficiary):
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
        null=True,
        blank=True
    )
    sub_project = models.ForeignKey(
        SubProject,
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )

    class Meta:
        abstract = False
        verbose_name = "Beneficiary Organization"
        verbose_name_plural = "Beneficiary Organizations"
