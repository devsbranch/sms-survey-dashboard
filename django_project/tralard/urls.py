# -*- coding: utf-8 -*-
from django.urls import path

from tralard.views.dashboard import HomeTemplateView
from tralard.views.project import (
    ProjectListView,
    SubProjectListView,
    SubProjectDetailView
)

from tralard.views.beneficiary import (
    BeneficiaryOrgListView,
    BeneficiaryOrgDetailView
)
from tralard.views.map import MapTemplateView

from tralard.views.fund import FundListAndCreateView, FundDetailView

app_name = 'tralard'
urlpatterns = [
    # home
    path('', HomeTemplateView.as_view(), name='home'),
    
    path(
        'map/', 
        MapTemplateView.as_view(), 
        name='map'
    ),

    # -------- project --------
    path(
        'project/list/', 
        ProjectListView.as_view(), 
        name='project_list'
    ),
    path(
        'project/subproject/list/', 
        SubProjectListView.as_view(), 
        name='sub_project_list'
    ),
    path(
        'project/subproject/detail/', 
        SubProjectDetailView.as_view(), 
        name='sub_project_detail'
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
    # -------- fund --------
    path(
        'fund/list/', 
        FundListAndCreateView.as_view(),
        name='fund-list'
    ),
    path(
        'beneficiary/<int:pk>/detail/', 
        FundDetailView.as_view(), 
        name='fund_detail'
    ),
]
