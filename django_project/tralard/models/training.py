# coding=utf-8
"""
Training model definitions for tralard app.
"""
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from tralard.models.sub_project import SubProject

logger = logging.getLogger(__name__)


class Training(models.Model):
    """
    Training and Training schedule definition.
    """
    sub_project = models.ForeignKey(
        SubProject,
        on_delete=models.CASCADE,
        verbose_name=_('Project name')
        )
    title = models.CharField(
        verbose_name=_('Title'),
        help_text=_('Titile of the Training'),
        blank=False,
        null=False,
        max_length=200,
    )
    notes = models.TextField(
        verbose_name=_('Training notes. Rich text editing is supported.'),
        help_text=_('Training notes.'),
        blank=False,
        null=False,
    )
    start_date = models.DateField(
        null=True,
        blank=False,
    )
    end_date = models.DateField(
        null=True,
        blank=False,
    )
    # noinspection PyClassicStyleClass.
    
    def __str__(self):
        return self.title
