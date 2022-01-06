# -*- coding: utf-8 -*-
from django.urls import path

from tralard.views.dashboard import HomeTemplateView
from tralard.views.program import ProgramDetailView
from tralard.views.project import (
    ProjectDetailView,
    SubProjectListView,
    SubProjectDetailView
)
from tralard.views.beneficiary import (
    BeneficiaryOrgListView,
    BeneficiaryOrgDetailView
)
from tralard.views.training import (
    TrainingListView,
    training_fetch,
    training_delete,
    template_testing,
)
from tralard.views.map import MapTemplateView
from tralard.views.fund import FundListAndCreateView, FundDetailView

app_name = 'tralard'
urlpatterns = [
    # home
    path('test/', template_testing, name='test'),
    
    path('', HomeTemplateView.as_view(), name='home'),
    
    path(
        'map/', 
        MapTemplateView.as_view(), 
        name='map'
    ),

    # -------- program --------
    path(
        'program/<slug:program_slug>/detail/', 
        ProgramDetailView.as_view(), 
        name='program-detail'
    ),
    # -------- project --------
    path(
        'project/subproject/list/', 
        SubProjectListView.as_view(), 
        name='sub_project_list'
    ),
    path(
        'program/<slug:program_slug>/project/<slug:project_slug>/detail/', 
        ProjectDetailView.as_view(), 
        name='project-detail'
    ),
    # -------- project fund --------
    path(
       'program/<slug:program_slug>/project/<slug:project_slug>/fund/',
        FundListAndCreateView.as_view(),
        name='fund-list'
    ),
    # -------- beneficiary --------
    
    # -------- training ------------
    path(
        'program/<slug:program_slug>/project/<slug:project_slug>/training/list/',
        TrainingListView.as_view(), 
        name='training-list'
    ),
    path(
        'program/<slug:program_slug>/project/<slug:project_slug>/training/<slug:training_entry_slug>/training/delete/', 
        training_delete,
        name='training-delete'
    ),
    path(
        'program/<slug:program_slug>/project/<slug:project_slug>/training/<slug:training_entry_slug>/training/fetch/', 
        training_fetch,
        name='training-fetch'
    ),
]