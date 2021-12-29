# coding=utf-8
"""
Program model definitions for tralard app.
"""
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from tralard.models.sub_project import SubProject
from dj_beneficiary.models import OrganizationBeneficiary as BaseOrganizationBeneficiary

from tinymce import HTMLField

logger = logging.getLogger(__name__)


class Beneficiary(BaseOrganizationBeneficiary):
    """
    Beneficiary Subclass object.
    """
    sub_project = models.ForeignKey(
        SubProject,
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )

    class Meta:
        # we hide its abstraction and reuse the object data. 
        abstract = False
        verbose_name = _('PPCR Beneficiary')
        verbose_name_plural = _('PPCR Beneficiaries')

    def __str__(self):
        return self.name.title()
