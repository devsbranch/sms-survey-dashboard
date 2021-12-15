# -*- coding: utf-8 -*-

from django.contrib import admin

from ppcr.models import (
   Program,
   Project,
   SubProject,
   Funding
)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(SubProject)
class SubProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Funding)
class FundingAdmin(admin.ModelAdmin):
    pass



