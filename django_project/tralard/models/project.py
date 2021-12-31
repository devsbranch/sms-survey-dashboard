# coding=utf-8
"""
Project model definitions for tralard app.
"""
import logging

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from tralard.models.program import Program

from tinymce import HTMLField

User = get_user_model()
logger = logging.getLogger(__name__)

class ApprovedProjectManager(models.Manager):
    """Custom manager that shows aproved projects."""
    def get_queryset(self):
        return super(
            ApprovedProjectManager, self
        ).get_queryset().filter(
            approved=True,)


class UnapprovedProjectManager(models.Manager):
    """Custom project manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            UnapprovedProjectManager, self).get_queryset().filter(
                approved=False)


class Representative(models.Model):
    """
    Project Representative.
    """
    GENDER_CHOICES = (
    ("Male", _("Male")),
    ("Female", _("Female")),
    ("Transgender", _("Transgender")),
    ("Other", _("Other"))
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    first_name = models.CharField(
        _("First Name"),
        max_length=200,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=200,
        null=False
    )
    birthdate = models.DateField(
        _("Birth Date"),
        auto_now_add=False,
        null=True,
        blank=True
    )
    gender = models.CharField(
        _("Gender"),
        max_length=50,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    address = HTMLField(
        help_text=_(
            'Address details and other information necesarry.'),
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Project(models.Model):
    """
    Project definition.
    """
    name = models.CharField(
        help_text=_('Name of this project.'),
        max_length=255,
        unique=True
    )
    description = models.CharField(
        help_text=_('A short description for the project'),
        max_length=500,
        blank=True,
        null=True
    )
    precis = HTMLField(
        help_text=_(
            'A detailed summary of the project. Rich text edditing is supported.'),
        blank=True,
        null=True
    )

    image_file = models.ImageField(
        help_text=_(
            'A banner image for this project. Most browsers support dragging '
            'the image directly on to the "Choose File" button above. The '
            'ideal size for your image is 512 x 512 pixels.'),
        upload_to='images/projects',
        blank=True
    )
    approved = models.BooleanField(
        help_text=_('Whether this project has been approved yet.'),
        default=False,
    )
    has_funding = models.BooleanField(
        help_text=_('Whether this project has an active funding.'),
        default=False,
    )
    focus_area = HTMLField(
        help_text=_(
            'Please describe the focus areas of the project.'
            '(if any). Rich text editing is supported'),
        blank=True,
        null=True
    )
    project_representative = models.ForeignKey(
        Representative,
        related_name='project_representative',
        help_text=_(
            'Project representative. '
            'This name will be used on trainings and any other references. '),
        on_delete=models.SET_NULL,
        blank=True,
        null=True  # This is needed to populate existing database.
    )
    project_managers = models.ManyToManyField(
        User, # import django default user model for now
        related_name='project_managers',
        blank=True,
        # null=True, null has no effect on ManyToManyField.
        help_text=_(
            'Managers of this project. '
            'They will be allowed to approve sub-projects in the '
            'fund distribution queue.'),
    )
    project_funders = models.ManyToManyField(
        User, # same here lets just hook into the default django User model for now
        related_name='funders',
        verbose_name='Project Funders',
        blank=True,
        # null=True, null has no effect on ManyToManyField.
        help_text=_(
            'Fund Managers of the project . '
            'These could either be funders or fundd managers, \
                will be allowed to approve sub-project supervisors and sub-project fund managers.'
            ),

    )
    training_managers = models.ManyToManyField(
        User,
        related_name='training_managers',
        blank=True,
        # null=True, null has no effect on ManyToManyField.
        help_text=_(
            'Managers of all trainings in this project. '
            'They will be allowed to create or remove training schedules.')
    )
    certification_managers = models.ManyToManyField(
        User,
        related_name='certification_managers',
        blank=True,
        # null=True, null has no effect on ManyToManyField.
        help_text=_(
            'Managers of the certifications in this project. '
            'They will receive email notification about projects and have'
            ' the same permissions as project owner.')
    )
    # Organisation where a project belongs, when the organisation is deleted,
    #  the project will automatically belongs to default organisation.
    program = models.ForeignKey(
        Program, 
        default='',
        on_delete=models.SET_DEFAULT,
    )
    objects = models.Manager()
    approved_objects = ApprovedProjectManager()
    unapproved_objects = UnapprovedProjectManager()

    # def get_absolute_url(self):
    #     """Return URL to project detail page
    #     :return: URL
    #     :rtype: str
        # """
        # return reverse('project-detail', kwargs={'pk': self.pk})
    def __str__(self):
        return self.name.title()
