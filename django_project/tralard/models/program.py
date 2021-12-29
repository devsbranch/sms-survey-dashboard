# coding=utf-8
"""
Program model definitions for tralard app.
"""
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Program(models.Model):
    """
    Program Definition i.e PPCR, TRALARD etc.
    """
    name = models.CharField(
        _("Program Name"),
        max_length=200,
        null=True,
        blank=True
    )
    approved = models.BooleanField(
        help_text=_('Whether this program has been approved yet.'),
        default=False,
        null=True,
        blank=True
    )
    started = models.DateField(
        _("Program Start Date"),
        auto_now_add=False,
        null=True,
        blank=True
    )
    description = models.TextField(
        help_text=_(
            'A detailed summary of the program. Rich text edditing is supported.'),
        max_length=2000,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name.title()
