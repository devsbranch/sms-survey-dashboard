# coding=utf-8
"""
Training model definitions for tralard app.
"""
import logging

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from tralard.models.sub_project import SubProject
from tralard.models.project import Representative

from tralard.utils import unique_slugify

from tinymce import HTMLField

logger = logging.getLogger(__name__)


class CompletedTrainingManager(models.Manager):
    """Custom manager that shows completed trainings."""
    def get_queryset(self):
        return super(
            CompletedTrainingManager, self
        ).get_queryset().filter(
            completed=True,)


class IncompletedTrainingManager(models.Manager):
    """Custom training manager that shows only incompleted trainings."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            IncompletedTrainingManager, self).get_queryset().filter(
                completed=False)

class TrainingType(models.Model):
    name = models.CharField(
        max_length=250, 
        blank=False, 
        default=''
    )

    def __str__(self):
        return self.name


class Training(models.Model):
    """
    Training and Training schedule definition.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    sub_project = models.ForeignKey(
        SubProject,
        on_delete=models.CASCADE,
        verbose_name=_('Project name')
    )
    title = models.CharField(
        verbose_name=_('Title'),
        help_text=_('Title of the Training'),
        max_length=200,
    )
    training_type = models.ForeignKey(
        TrainingType,
        on_delete=models.CASCADE,
        verbose_name=_('Training Type'),
        null=True,
        blank=True
    )
    start_date = models.DateField(
        null=True,
        blank=True,
    )
    end_date = models.DateField(
        null=True,
        blank=True,
    )
    notes = models.TextField(
        verbose_name=_('Training notes. Rich text editing is supported.'),
        help_text=_('Training notes.'),
        blank=True,
        null=True,
    )
    moderator = models.ForeignKey(
        'tralard.representative',
        on_delete=models.SET_NULL,
        help_text=_(
            'Training Moderator. '
            'This is the person supervising and or conducting the training, the name will be used on trainings and any other references. '),
        blank=True,
        null=True  # This is needed to populate existing database.
    )
    completed = models.BooleanField(
        help_text=_('Has this Training schedule been conducted andd completed?'),
        default=False,
    )
    objects = models.Manager()
    completed_objects = CompletedTrainingManager()
    incompleted_objects = IncompletedTrainingManager()


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)


class Attendance(models.Model):
    male_count = models.IntegerField(
        _("Number of Males that attended the training."),
        null=True, 
        blank=True, 
    )
    female_count = models.IntegerField(
        _("Number of Males that attended the training."),
        null=True, 
        blank=True, 
    )
    notes = HTMLField(
        verbose_name=_('Training Outcome notes. Rich text editing is supported.'),
        help_text=_('Training Outcome notes.'),
        blank=False,
        null=False,
    )
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        verbose_name=_('Project name'), 
        null=True,
        blank=True
    )
    def __str__(self):
        return f'Males: {self.male_count}, Females: {self.female_count}'
