from django.contrib import admin

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
    Expenditure,
    Disbursement,
)


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
admin.site.register(Attendance)
admin.site.register(Expenditure)
admin.site.register(Beneficiary)
admin.site.register(TrainingType)
admin.site.register(Disbursement)
admin.site.register(Representative)
