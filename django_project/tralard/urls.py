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

app_name = 'tralard'
urlpatterns = [
    # home
    path('', HomeTemplateView.as_view(), name='home'),

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

]
