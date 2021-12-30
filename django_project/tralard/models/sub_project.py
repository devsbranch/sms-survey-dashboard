# coding=utf-8
"""
Sub Project model definitions for tralard app.
"""
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from tralard.models.project import Project, Representative

from tinymce import HTMLField

logger = logging.getLogger(__name__)


class Indicator(models.Model):
    """
    Sub Project Indicator Representative.
    """
   
    name = models.CharField(
        _("Name"),
        max_length=200,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.name.lower()


class SubProject(models.Model):
    """
    Sub Project definition.
    """
    name = models.CharField(
        help_text=_('Name of this Sub Project.'),
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )
    size = HTMLField(
        help_text=_(
            'Size (number of Hectors, SquareMeters, Products etc,).'),
        max_length=2000,
        blank=True,
        null=True
    )
    description = HTMLField(
        help_text=_(
            'A detailed summary of the Sub Project. Rich text edditing is supported.'),
        max_length=2000,
        blank=True,
        null=True
    )
    approved = models.BooleanField(
        help_text=_('Whether this project has been approved yet.'),
        default=False,
        null=True,
        blank=True
    )
    focus_area = HTMLField(
        help_text=_(
            'Please describe the focus areas of the project.'
            '(if any). Rich text editing is supported'),
        max_length=10000,
        blank=True,
        null=True
    )
    supervisor = models.ForeignKey(
        Representative,
        help_text=_(
            'Sub Project Supervisor. '
            'This name will be used on trainings and any other references. '),
        on_delete=models.SET_NULL,
        blank=True,
        null=True  # This is needed to populate existing database.
    )
    training_moderators = models.ManyToManyField(
        Representative,
        related_name='training_moderators',
        blank=True,
        # null=True, null has no effect on ManyToManyField.
        help_text=_(
            'Managers of all trainings in this Sub project. '
            'They will be allowed to create or remove training schedules.')
    )
    # Organisation where a project belongs, when the organisation is deleted,
    #  the project will automatically belongs to default organisation.
    image_file = models.ImageField(
        help_text=_(
            'A banner image for this Sub Project. Most browsers support dragging '
            'the image directly on to the "Choose File" button above. The '
            'ideal size for your image is 512 x 512 pixels.'),
        upload_to='images/projects',
        blank=True
    )
    project = models.ForeignKey(
        Project, 
        default='',
        null=True,
        blank=True,
        on_delete=models.SET_DEFAULT,
    )
    indicators = models.ManyToManyField(
        Indicator,
        related_name='subproject_indicators',
        blank=True,
        # null=True, null has no effect on ManyToManyField.
    )
    # def get_absolute_url(self):
    #     """Return URL to project detail page
    #     :return: URL
    #     :rtype: str
        # """
        # return reverse('project-detail', kwargs={'pk': self.pk})
    def __str__(self):
        return self.name.title()
        
    @property 
    def get_related_project(self):
        return self.project.name