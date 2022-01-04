# coding=utf-8
"""
Project model definitions for tralard app.
"""
import logging

from django.db import models
from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from tralard.utils import unique_slugify

from tralard.models.fund import Fund

# (TODO:Alison) take the get_related_sub_project method to utilities or model managers.
# not very safe (circular import issue candidate) 
# except that we are referencing to project under subproject via string reference 
# and not by imoprt - so its safe this way
from tralard.models.sub_project import SubProject
from tralard.models.beneficiary import Beneficiary


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
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    first_name = models.CharField(
        _("First Name"),
        max_length=200,
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
    email = models.EmailField(
        _("Email"),
        null=True,
        blank=True
    )
    cell = models.CharField(
        _("Cell"),
        max_length=50,
        null=True,
        blank=True
    )
    ward = models.ForeignKey(
        'tralard.ward', 
        default='',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    address = HTMLField(
        help_text=_(
            'Address details and other information necesarry.'),
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(f"{self.first_name} {self.last_name}"))
        super().save(*args, **kwargs)


class Project(models.Model):
    """
    Project definition.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    name = models.CharField(
        help_text=_('Name of this project.'),
        max_length=255,
        unique=True
    )
    approved = models.BooleanField(
        help_text=_('Whether this project has been approved yet.'),
        default=False,
    )
    has_funding = models.BooleanField(
        help_text=_('Whether this project has an active funding.'),
        default=False,
    )
    description = models.CharField(
        help_text=_('A short description for the project'),
        max_length=500,
        blank=True,
        null=True
    )
    program = models.ForeignKey(
        'tralard.program', 
        default='',
        on_delete=models.CASCADE,
    )
    project_representative = models.ForeignKey(
        Representative,
        related_name='project_representatives',
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
    image_file = models.ImageField(
        help_text=_(
            'A banner image for this project. Most browsers support dragging '
            'the image directly on to the "Choose File" button above. The '
            'ideal size for your image is 512 x 512 pixels.'),
        upload_to='images/projects',
        blank=True
    )
    precis = HTMLField(
        help_text=_(
            'A detailed summary of the project. Rich text edditing is supported.'),
        blank=True,
        null=True
    )

    focus_area = HTMLField(
        help_text=_(
            'Please describe the focus areas of the project.'
            '(if any). Rich text editing is supported'),
        blank=True,
        null=True
    )
    objects = models.Manager()
    approved_objects = ApprovedProjectManager()
    unapproved_objects = UnapprovedProjectManager()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to project detail page
        :return: URL
        :rtype: str
        """
        return reverse_lazy('tralard:project-detail', 
            kwargs={
                'program_slug': self.program.slug, 
                'project_slug': self.slug
                }
            )
 
    @property
    def get_related_sub_projects(self):
        sub_projects_queryset = SubProject.objects.filter(
            project__slug=self.slug
            )
        return sub_projects_queryset

    @property
    def count_sub_projects(self):
        sub_projects_count_queryset = SubProject.objects.filter(
            project__slug=self.slug
            ).count()
        return sub_projects_count_queryset

    @property
    def count_beneficiaries(self):
        beneficiary_count_queryset = Beneficiary.objects.filter(
            sub_project__project__slug=self.slug
            ).count()
        return beneficiary_count_queryset

    @property
    def get_total_project_fund(self):
        """Computes total funds related to this project."""
        related_funds_sum_qs = Fund.objects.filter(
            project__slug=self.slug
        ).aggregate(Sum('amount'))

        amount_value = related_funds_sum_qs['amount__sum']
        return amount_value

    @property
    def get_total_fund_balance(self):
        """Computes total funds balance related to this project."""
        related_funds_sum_qs = Fund.objects.filter(
            project__slug=self.slug
        ).aggregate(Sum('balance'))

        amount_value = related_funds_sum_qs['balance__sum']
        return amount_value



class Feedback(models.Model):
    """
    Project Feedback.
    """
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    title = models.CharField(
        _("Title"),
        max_length=200,
    )
    date = models.DateField(
        _("Create Date"),
        auto_now_add=False,
        null=True,
        blank=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    moderator = models.ForeignKey(
        Representative,
        related_name='feedback_moderator',
        help_text=_(
            'Feedback Moderator. '
            'This name will be used on project feedback and any other references. '),
        on_delete=models.SET_NULL,
        blank=True,
        null=True  
    )
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} project: {self.project.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)

