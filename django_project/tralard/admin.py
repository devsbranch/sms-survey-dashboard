from django.contrib import admin

from tralard.models import (
    Fund, 
    Program, 
    Project, 
    SubProject, 
    Training,
    TrainingType,
    Attendance,
    FollowUp,
    Beneficiary,
    FundExpenditure,
    FundDisbursed,
)


admin.site.register(Fund)
admin.site.register(Program)
admin.site.register(Project)
admin.site.register(SubProject)
admin.site.register(Training)
admin.site.register(TrainingType)
admin.site.register(Attendance)
admin.site.register(FollowUp)
admin.site.register(Beneficiary)
admin.site.register(FundExpenditure)
admin.site.register(FundDisbursed)
