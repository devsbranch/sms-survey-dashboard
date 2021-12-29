# coding=utf-8
"""
Sub Project model definitions for tralard app.
"""
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from tralard.models.sub_project import SubProject


logger = logging.getLogger(__name__)


class FollowUp(models.Model):
    """
    Sub Project Progress Follow Up Action.
    """
    implementation_status = models.CharField(
        help_text=_(
            'Project implementation status in line with project workplan & procurement plan.'),
        max_length=255,
        blank=True,
        null=True
    )
    follow_up_action = models.CharField(
        help_text=_(
            'Follow up action.'),
        max_length=255,
        blank=True,
        null=True
    )
    follow_up_action_personnel = models.TextField(
        help_text=_(
            'Who will conduct what follow up action items.'),
        max_length=255,
        blank=True,
        null=True
    )
    follow_up_action_date = models.DateField(
        help_text=_(
            'Date to conduct the next follow up.'),
        blank=True,
        null=True
    )
    comments = models.TextField(
        help_text=_(
            'Comments (If project is complete, has completion certificate been issued, when?).'),
        max_length=255,
        blank=True,
        null=True
    )
    sub_project = models.ForeignKey(
        SubProject,
        help_text=_(
            'Sub Project to follow up.'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True  # This is needed to populate existing database.
    )
    def __str__(self):
        return self.implementation_status[:15]
