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
    TrainingCreateView,
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
       'program/<slug:program_slug>/project/<slug:project_slug>/funds/',
        FundListAndCreateView.as_view(),
        name='fund-list'
    ),
    # -------- beneficiary --------
    path(
        'beneficiary/list/', 
        BeneficiaryOrgListView.as_view(), 
        name='beneficiary_list'
    ),
    path(
        'beneficiary/detail/', 
        BeneficiaryOrgDetailView.as_view(), 
        name='beneficiary_detail'
    ),
    # -------- training ------------
    path(
        'training/list/', 
        TrainingListView.as_view(), 
        name='training-list'
    ),
    path(
        'training/delete/<slug:training_slug>/', 
        training_delete, 
        name='training-delete'
    ),
    path(
        'training/create/', 
        TrainingCreateView.as_view(), 
        name='training-create'
    ),
    path(
        'beneficiary/<slug:beneficiary_slug>/detail/', 
        FundDetailView.as_view(), 
        name='fund_detail'
    ),
]
