from django.contrib import admin
from django.contrib.gis.db import models

from mapwidgets.widgets import GooglePointFieldWidget

from tralard.models import (
    Fund, 
    Program, 
    Project, 
    Feedback, 
    SubProject, 
    Training,
    TrainingType,
    Attendance,
    FollowUp,
    Beneficiary,
    Representative,
    Province,
    District,
    Ward,
    Indicator,
    Expenditure,
    Disbursement,
)
from tralard.models.profile import Profile

CUSTOM_MAP_SETTINGS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocation", [-15.7177013, 28.6300491]),
    ),
}

class BeneficiaryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
    }


admin.site.register(Fund)
admin.site.register(Ward)
admin.site.register(Program)
admin.site.register(Project)
admin.site.register(Feedback)
admin.site.register(Training)
admin.site.register(FollowUp)
admin.site.register(District)
admin.site.register(Province)
admin.site.register(SubProject)
admin.site.register(Indicator)
admin.site.register(Attendance)
admin.site.register(Expenditure)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(TrainingType)
admin.site.register(Disbursement)
admin.site.register(Representative)
admin.site.register(Profile)
