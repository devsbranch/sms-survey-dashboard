# coding=utf-8
"""
Project model definitions for tralard app.
"""
import logging

from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from tralard.utils import unique_slugify

from tinymce import HTMLField

User = get_user_model()
logger = logging.getLogger(__name__)


class Project(models.Model):
    """
    Project Definition i.e PPCR, TRALARD etc.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    name = models.CharField(
        _("Project Name"),
        max_length=200,
        unique=True
    )
    approved = models.BooleanField(
        help_text=_('Whether this project has been approved yet.'),
        default=False,
        null=True,
        blank=True
    )
    started = models.DateField(
        _("project Start Date"),
        auto_now_add=False,
        null=True,
        blank=True
    )
    project_representative = models.ForeignKey(
        User,
        related_name='project_representatives',
        help_text=_(
            'project representative. '
            'This name will be used on projects and any other references. '),
        on_delete=models.SET_NULL,
        blank=True,
        null=True  # This is needed to populate existing database.
    )
    logo = models.ImageField(
        help_text=_(
            'A banner image for this project. Most browsers support dragging '
            'the image directly on to the "Choose File" button above. The '
            'ideal size for your image is 512 x 512 pixels.'),
        upload_to='images/projects',
        blank=True
    )
    description = HTMLField(
        help_text=_(
            'A detailed summary of the project. Rich text edditing is supported.'),
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name.title()

    # def get_absolute_url(self):
    #     return reverse_lazy('tralard:project-detail', kwargs={'project_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)
