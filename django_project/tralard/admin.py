from django.contrib import admin
from django.contrib.gis.db import models

from mapwidgets.widgets import GooglePointFieldWidget
from import_export.admin import ImportExportActionModelAdmin
from dj_beneficiary.models import (
    Agent,
    Facility,
    FacilityType,
    ImplementingPartner
)

from tralard.models import (
    Ward,
    Fund,
    Program,
    Project,
    District,
    FollowUp,
    Province,
    Feedback,
    Training,
    Indicator,
    Attendance,
    SubProject,
    Beneficiary,
    Expenditure,
    Disbursement,
    TrainingType,
    IndicatorTarget,
    IndicatorTargetValue,
)
from tralard.resources import (
    FundResource,
    WardResource,
    ProgramResource,
    ProjectResource,
    TrainingResource,
    ProvinceResource,
    DistrictResource,
    IndicatorResource,
    SubProjectResource,
    BeneficiaryResource,
    ExpenditureResource,
    TrainingTypeResource,
    DisbursementResource,
    IndicatorTargetResource,
    IndicatorTargetValueResource,
)
from tralard.models.profile import Profile
from tralard.constants import CUSTOM_MAP_SETTINGS

# Abstruct these from admin dashboard 
# as we do not need them.
admin.site.unregister(Agent)
admin.site.unregister(Facility)
admin.site.unregister(FacilityType)
admin.site.unregister(ImplementingPartner)


class BeneficiaryAdmin(ImportExportActionModelAdmin):
    resource_class = BeneficiaryResource

    formfield_overrides = {
        models.PointField: {
            "widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)
        }
    }
    empty_value_display = "-empty-"
    list_display = [
        "name",
        "org_type",
        "total_beneficiaries",
        "total_females",
        "total_males",
        "total_hhs",
        "female_hhs",
        "below_sixteen",
        "sixteen_to_thirty",
        "thirty_to_fourty_five",
        "above_fourty_five",
        "email",
        "cell",
        "registered_date",
        "created",
        "location",
        "ward",
        "sub_project",
    ]
    list_filter = (
        "name", 
        "org_type", 
        "email", 
        "cell", 
        "ward", 
        "sub_project"
    )
    search_fields = [
        "name", 
        "email", 
        "cell", 
    ]


class FundAdmin(ImportExportActionModelAdmin):
    resource_class = FundResource
    empty_value_display = "-empty-"
    list_display = [
        "amount",
        "approved",
        "approval_status",
        "balance_currency",
        "balance",
        "variation_currency",
        "variation",
        "funding_date",
        "currency",
        "sub_project",
        "requested_by",
        "approved_by",
        "approved_date",
        "created",
    ]
    list_filter = [
        "amount",
        "approved",
        "approval_status",
        "balance",
        "currency",
        "sub_project",
        "requested_by",
        "approved_by",
    ]
    search_fields = [
        "amount",
        "approved",
        "balance",
        "currency",
    ]


class DisbursementAdmin(ImportExportActionModelAdmin):
    resource_class = DisbursementResource
    empty_value_display = "-empty-"
    list_display = [
        "amount",
        "balance_currency",
        "balance",
        "disbursement_date",
        "currency",
        "fund",
        "created",
    ]
    list_filter = [
        "amount",
        "balance",
        "disbursement_date",
        "currency",
        "fund",
    ]
    search_fields = [
        "amount",
        "balance",
        "currency",
    ]


class ExpenditureAdmin(ImportExportActionModelAdmin):
    resource_class = ExpenditureResource
    empty_value_display = "-empty-"
    list_display = [
        "amount", 
        "expenditure_date", 
        "currency", 
        "disbursment", 
        "created"
    ]
    list_filter = (
        "amount",
        "currency",
        "disbursment",
    )
    search_fields = [
         "amount",
        "currency",
    ]


class ProvinceAdmin(ImportExportActionModelAdmin):
    resource_class = ProvinceResource
    empty_value_display = "-empty-"
    list_display = ["name", "location"]
    list_filter = ("name",)
    search_fields = ['name']


class DistrictAdmin(ImportExportActionModelAdmin):
    resource_class = DistrictResource
    empty_value_display = "-empty-"
    list_display = [
        "name",
        "location",
        "province",
        "created",
    ]
    list_filter = (
        "name",
        "province",
    )
    search_fields = ["name"]


class WardAdmin(ImportExportActionModelAdmin):
    resource_class = WardResource
    empty_value_display = "-empty-"
    list_display = [
        "name",
        "district",
        "location",
        "created",
    ]
    list_filter = ("name",)
    search_fields = ['name']


class ProgramAdmin(ImportExportActionModelAdmin):
    resource_class = ProgramResource
    empty_value_display = "-empty-"
    list_display = [
        "name",
        "approved",
        "started",
        "program_representative",
    ]
    list_filter = (
        "name",
        "approved",
        "program_representative",
    )
    search_fields = [
        "name",
        "approved",
    ]


class ProjectAdmin(ImportExportActionModelAdmin):
    resource_class = ProjectResource
    empty_value_display = "-empty-"
    list_display = [
        "name",
        "approved",
        "has_funding",
        "status",
        "program",
        "project_representative",
    ]
    list_filter = (
        "name",
        "approved",
        "has_funding",
        "status",
        "program",
        "project_representative",
    )
    search_fields = [
        "name",
        "approved",
        "has_funding",
        "status",
    ]


class SubProjectAdmin(ImportExportActionModelAdmin):
    resource_class = SubProjectResource
    empty_value_display = "-empty-"
    list_display = [
        "name",
        "size",
        "ward",
        "status",
        "project",
        "approved",
        "representative",
    ]
    list_filter = (
        "name",
        "size",
        "ward",
        "status",
        "project",
        "approved",
        "representative",
    )
    search_fields = [
        "name",
        "size",
        "ward",
        "status",
        "approved",
    ]


class TrainingAdmin(ImportExportActionModelAdmin):
    resource_class = TrainingResource
    empty_value_display = "-empty-"
    list_displlay = [
        "title",
        "sub_project",
        "start_date",
        "end_date",
        "moderator",
        "training_type",
        "completed",
    ]
    list_filter = (
        "title",
        "sub_project",
        "start_date",
        "end_date",
        "moderator",
        "training_type",
        "completed",
    )
    search_fields = [
        "title",
        "start_date",
        "end_date",
        "completed",
    ]


class IndicatorAdmin(ImportExportActionModelAdmin):
    resource_class = IndicatorResource
    empty_value_display = "-empty-"
    list_display = ["name"]
    list_filter = ("name",)
    search_fields = ['name']


class ExpenditureAdmin(ImportExportActionModelAdmin):
    resource_class = ExpenditureResource
    empty_value_display = "-empty-"
    list_display = [
        "amount", 
        "currency", 
        "disbursment", 
        "expenditure_date", 
        "created"
    ]
    list_filter = (
        "amount",
        "currency",
        "disbursment",
    )
    search_fields = [
        "amount",
        "currency",
    ]


class TrainingTypeAdmin(ImportExportActionModelAdmin):
    resource_class = TrainingTypeResource
    empty_value_display = "-empty-"
    list_display = ["name"]
    list_filter = ("name",)
    search_fields = ['name']


class IndicatorTargetAdmin(ImportExportActionModelAdmin):
    resource_class = IndicatorTargetResource
    empty_value_display = "-empty-"
    list_display = [
        "unit_of_measure", 
        "baseline_value", 
        "indicator"
    ]
    list_filter = (
        "unit_of_measure",
        "baseline_value",
        "indicator",
    )
    search_fields = [
        "unit_of_measure",
        "baseline_value",
    ]


class IndicatorTargetValueAdmin(ImportExportActionModelAdmin):
    resource_class = IndicatorTargetValueResource
    empty_value_display = "-empty-"
    list_display = [
        "year", 
        "target_value", 
        "actual_value", 
        "indicator_target"
    ]
    list_filter = (
        "year",
        "target_value",
        "actual_value",
        "indicator_target",
    )
    search_fields = [
        "year",
        "target_value",
    ]


admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(FollowUp)
admin.site.register(Attendance)
admin.site.register(Fund, FundAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(SubProject, SubProjectAdmin)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(Expenditure, ExpenditureAdmin)
admin.site.register(Disbursement, DisbursementAdmin)
admin.site.register(TrainingType, TrainingTypeAdmin)
admin.site.register(IndicatorTarget, IndicatorTargetAdmin)
admin.site.register(IndicatorTargetValue, IndicatorTargetValueAdmin)
