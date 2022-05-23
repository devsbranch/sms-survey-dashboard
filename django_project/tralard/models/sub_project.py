# coding=utf-8
"""
Sub Project model definitions for tralard app.
"""
import json
import logging
import datetime

from django.db import models
from django.utils.text import slugify
from django.db.models.aggregates import Sum
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField

from tralard.models.fund import Fund
from tralard.models.ward import Ward
from tralard.utils import (
    unique_slugify,
    sub_project_update_form,
    sub_project_create_form,
)
from tralard.models.training import Training
from tralard.models.province import Province
from tralard.models.beneficiary import Beneficiary
from tralard.constants import PROJECT_STATUS_CHOICES, MODEL_FIELD_CHOICES

User = get_user_model()
logger = logging.getLogger(__name__)


class SubProjectManager(models.Manager):
    """ Custom manager that aggregates subcomponents and subprojects provincial overview. """

    def get_sub_projects_district_json(self):
        """ Queryset to aggregate suprojects in each province """
        province_labels = []
        sub_projects_count = []

        for province in Province.objects.all():
            total_subs = self.filter(ward__district__province__name=province.name).count()

            province_labels.append(province.name)
            sub_projects_count.append(total_subs)

        province_labels_json = json.dumps(province_labels)
        sub_projects_count_json = json.dumps(sub_projects_count)

        return {
            "labels": province_labels_json,
            "data": sub_projects_count_json
        }

    def get_subcomponents_in_district_json(self):
        """ Queryset to aggregate subcomponents in each province """
        province_labels = []
        subcomponents_count = []
        subcomponent_names = []

        #  Get Sub projects in province
        for province in Province.objects.all():
            total_subs = self.filter(ward__district__province__name=province.name)
            province_labels.append(province.name)

            for subproject in total_subs:
                subcomponent_names.append(subproject.subcomponent.name)

            unique_subproject_names = list(set(subcomponent_names))
            subcomponents_count.append(len(unique_subproject_names))

        province_labels_json = json.dumps(province_labels)
        subcomponents_count_json = json.dumps(subcomponents_count)

        return {
            "labels": province_labels_json,
            "data": subcomponents_count_json,
        }


class CountProjects(models.Manager):
    """ Custom manager that aggregates subcomponents in each province. """


class SubProject(models.Model):
    """
    Sub Project definition.
    """

    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    name = models.CharField(
        help_text=_("Name of this SubProject."),
        max_length=255,
        unique=True
    )
    size = models.DecimalField(
        help_text=_("Capture project data in quantity i.e. 2, 3.7, 159.44"),
        decimal_places=3,
        max_digits=10,
        blank=True,
        null=True,
    )
    size_description = models.TextField(
        help_text=_("A brief description of the project size i.e. 24 Hectors of Land"),
        max_length=500,
        blank=True,
        null=True,
    )
    ward = models.ForeignKey(
        Ward,
        help_text=_('The ward in which this SubProject has been implemented.'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    representative = models.ForeignKey(
        User,
        help_text=_(
            "Sub Project Supervisor. "
            "This name will be used on trainings and any other references. "
        ),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,  # This is needed to populate existing database.
    )
    subcomponent = models.ForeignKey(
        "tralard.SubComponent",
        default="",
        on_delete=models.CASCADE,
    )
    managers = models.ManyToManyField(
        User,
        related_name="subproject_managers",
        blank=True,
        # null=True, null has no effect on ManyToManyField.
        help_text=_(
            "Managers of all trainings and project activities in this Sub project. "
            "They will be allowed to create or delete SubProject data."
        ),
    )
    approved = models.BooleanField(
        # changed to True beccause the create feature
        # of subproject shall be accessible at admdin level only
        # and all created subprojects by admins are preaproved.
        default=True,
        null=True,
        blank=True,
    )
    status = models.CharField(
        _("Project Status"),
        max_length=50,
        choices=PROJECT_STATUS_CHOICES,
        null=True,
        blank=True,
    )
    image_file = models.ImageField(
        help_text=_(
            "A banner image for this Sub Project. Most browsers support dragging "
            'the image directly on to the "Choose File" button above. The '
            "ideal size for your image is 512 x 512 pixels."
        ),
        upload_to="images/subcomponents",
        blank=True,
    )
    description = models.TextField(
        help_text=_(
            "A detailed summary of the SubProject. Rich text edditing is supported."
        ),
        max_length=2000,
        blank=True,
        null=True,
    )
    focus_area = models.TextField(
        help_text=_(
            "Please describe the focus areas of the SubProject."
            "(if any). Rich text editing is supported"
        ),
        max_length=10000,
        blank=True,
        null=True,
    )
    latitude = models.DecimalField(
        null=True,
        blank=True,
        max_digits=8,
        decimal_places=5,
        help_text="Enter the latitude coordinate. For example -14.09233"
    )
    longitude = models.DecimalField(
        null=True,
        blank=True,
        max_digits=8,
        decimal_places=5,
        help_text="Enter the latitude coordinate. For example 27.09233"
    )
    created = models.DateTimeField(auto_now_add=True)


longitude = models.FloatField(
    help_text='this number must be in Decimal degrees (DD) e.g 65.1189',
    blank=True,
    null=True,
)
latitude = models.FloatField(
    help_text='this number must be in Decimal degrees (DD) e.g 44.94',
    blank=True,
    null=True,
)
objects = models.Manager()
custom_objects = SubProjectManager()


def __str__(self):
    return self.name.title()


def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = unique_slugify(self, slugify(self.name))
    super().save(*args, **kwargs)


@property
def get_related_project(self):
    return self.subcomponent.name


@property
def fund_utilization_percent(self):
    subcomponent_id = self.subcomponent.id
    funds_amount_qs = Fund.objects.filter(sub_project__slug=self.slug).aggregate(
        Sum("amount")
    )

    funds_balance_qs = Fund.objects.filter(sub_project__slug=self.slug).aggregate(
        Sum("balance")
    )
    amount_value = funds_amount_qs["amount__sum"]
    balance_value = funds_balance_qs["balance__sum"]
    if amount_value is not None and balance_value is not None:
        fund_utilization_percent = (
                                           float(balance_value) / float(amount_value)
                                   ) * 100
    else:
        fund_utilization_percent = 0
    return round(fund_utilization_percent)


@property
def count_beneficiaries(self):
    beneficiary_count_queryset = Beneficiary.objects.filter(
        sub_project__slug=self.slug
    ).count()
    return beneficiary_count_queryset


@property
def count_training_schedules(self):
    training_entries_qs = Training.objects.filter(
        sub_project__slug=self.slug
    ).count()
    return training_entries_qs


@property
def get_total_sub_project_fund(self):
    """Computes total funds related to this SubProject."""
    related_funds_sum_qs = Fund.objects.filter(
        sub_project__slug=self.slug
    ).aggregate(Sum("amount"))

    amount_value = related_funds_sum_qs["amount__sum"]
    return amount_value


@property
def sub_project_update_form(self):
    """Assigns a form to SubProject after create."""
    form = sub_project_update_form(self)
    return form


@property
def subproject_manage_url(self):
    url = f"/program/{self.project.program.slug}/project/{self.project.slug}/subproject/{self.slug}/manage/"
    return url


class Photo(models.Model):
    """Image model for subproject photos"""
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    image = FilerImageField(
        null=False,
        db_column="img_id",
        on_delete=models.CASCADE
    )
    progress_status = models.ForeignKey(
        'tralard.ProgressStatus',
        default="",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.image} {self.name}"

    @property
    def get_image(self):
        return self.image.file

    @property
    def get_images(self):
        return self.image

    @property
    def sub_project_create_form(self):
        """Assigns a form to SubProject after create."""
        form = sub_project_create_form()
        return "Hello form"


class ProgressStatus(models.Model):
    """SubProject status trail model."""
    status = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=PROJECT_STATUS_CHOICES
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    subproject = models.ForeignKey(
        'tralard.SubProject',
        on_delete=models.CASCADE
    )
    is_completed = models.BooleanField(default=False)
    created = models.DateField(
        auto_now_add=False,
        default=datetime.datetime.now
    )
    timestamp = models.DateTimeField(
        auto_now_add=False,
        default=datetime.datetime.now
    )

    class Meta:
        verbose_name = _("Progress Status")
        verbose_name_plural = _("Progress Statuses")

    def __str__(self):
        return f"{self.status} {self.created}"
