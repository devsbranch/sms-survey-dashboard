from django.contrib import admin

from tralard.models import (
    Fund, 
    Program, 
    Project, 
    SubProject, 
    Training
)


admin.site.register(Fund)
admin.site.register(Program)
admin.site.register(Project)
admin.site.register(SubProject)
admin.site.register(Training)
