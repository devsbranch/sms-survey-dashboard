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
            "data" : sub_projects_count_json
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
            "data" : subcomponents_count_json,
        }     

class CountProjects(models.Manager):
    """ Custom manager that aggregates subcomponents in each province. """
    
 
class Indicator(models.Model):
    """
    Sub Project Indicator Representative.
    """
       
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True,
    )
    name = models.CharField(
        _("Name"),
        max_length=200,
    )

    def __str__(self):
        return self.name.lower()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)


class IndicatorTarget(models.Model):
    """
    Stores a single Indicator target entry, related to model 'Indicator'.
    """
    unit_of_measure = models.ForeignKey(
        "tralard.IndicatorUnitOfMeasure", 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True,
        help_text="A brief description of this indicator target.",
    )
    baseline_value = models.CharField(
        _("Baseline Value"),
        max_length=200,
        null=True,
        blank=True,
        help_text="A baseline is data or measurement that is collected prior to the implementation of the project.",
    )
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description[:75]}| {self.unit_of_measure} Target"


class IndicatorTargetValue(models.Model):
    year =  models.DateField(_('Target Year'))
    target_value =  models.CharField(
        _('Target Value'),
        max_length=200,
        default=0
    )
    indicator_target =  models.ForeignKey(
        IndicatorTarget,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.indicator_target.description} Target for: {self.year.year}"


class IndicatorUnitOfMeasure(models.Model):
    unit_of_measure = models.CharField(
        _("Unit of Measure"), max_length=200,
        null=True,
        blank=True
    )
    data_source = models.CharField(
        _("Source of data"), 
        max_length=200,
        choices=MODEL_FIELD_CHOICES
    )

    def __str__(self):
        return self.unit_of_measure
    
    def get_actual_data(self, indicator_obj):
        """
        This method returns data to be used in the indicator report. This data
        returned is a number which is a Sum total of the field data for all Sub Projects
        under the given Indicator.
        """

        sub_project_filter = {"sub_project__indicators": indicator_obj}
        
        total = 0

        if self.data_source == "size":
            filter_by = {"indicators": indicator_obj}
            try:
                total = float(SubProject.objects.filter(**filter_by).aggregate(Sum('size'))['size__sum'])
            except TypeError:
                total = 0

        elif self.data_source == "total_beneficiaries":
            total = Beneficiary.custom_objects.get_total_beneficiaries(sub_project_filter)

        elif self.data_source == "total_females":
            total = Beneficiary.custom_objects.get_total_females(sub_project_filter)
        
        elif self.data_source == "total_males":
            total = Beneficiary.custom_objects.get_total_males(sub_project_filter)
        
        elif self.data_source == "total_hhs":
            total = Beneficiary.custom_objects.get_total_hhs(sub_project_filter)
        
        elif self.data_source == "female_hhs":
            total = Beneficiary.custom_objects.get_female_hhs(sub_project_filter)
        elif self.data_source == "beneficiary_orgs":
            total = Beneficiary.objects.filter(**sub_project_filter).count()

        return total
        

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
        help_text=_("Size (number of Hectors, SquareMeters, Products etc)."),
        decimal_places=3,
        max_digits=10,
        blank=True,
        null=True,
    )
    size_description = models.TextField(
        help_text=_("A brief description of the project size, like what the size implies."),
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
    indicators = models.ManyToManyField(
        Indicator,
        related_name="indicator_related_subprojects",
        blank=True,
        # null=True, null has no effect on ManyToManyField.
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
    created = models.DateTimeField(auto_now_add=True)
    
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
    def count_indicators(self):
        indicator_related_subprojects = Indicator.objects.filter(
            indicator_related_subprojects__slug=self.slug
        ).count()
        return indicator_related_subprojects

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
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.image} {self.name}"

    @property
    def get_image(self):
        return self.image.file

    @property
    def sub_project_create_form():
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
    photos  = models.ManyToManyField(
        'tralard.Photo',
        blank=True,
        related_name='progress_statuses'
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
    
    class Meta:
        verbose_name = _("Progress Status")
        verbose_name_plural = _("Progress Statuses")

    def __str__(self):
        return f"{self.status} {self.created}"
