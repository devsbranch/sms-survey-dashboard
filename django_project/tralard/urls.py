# -*- coding: utf-8 -*-
from django.urls import path
from tralard.views.dashboard import HomeTemplateView
from tralard.views.program import ProgramDetailView
from tralard.views.project import (
    ProjectDetailView,
    SubProjectListView,
    SubProjectDetailView,
    delete_sub_project,
    update_sub_project,
    create_feedback,
    edit_feedback,
    delete_feedback,
    create_project,
    update_project,
    delete_project,
)
from tralard.views.beneficiary import BeneficiaryOrgListView, BeneficiaryOrgDetailView
from tralard.views.beneficiary import BeneficiaryOrgListView, BeneficiaryOrgDetailView
from tralard.views.training import (
    TrainingListView,
    training_fetch,
    training_delete,
    template_testing,
)
from tralard.views.map import MapTemplateView
from tralard.views.fund import (
    FundListAndCreateView,
    FundDetailView,
    delete_disbursement,
    fund_delete,
    fund_detail,
    update_disbursement,
    update_fund,
)

app_name = "tralard"
urlpatterns = [
    # home
    path(
        "test/",
        template_testing,
        name="test",
    ),
    path(
        "",
        HomeTemplateView.as_view(),
        name="home",
    ),
    path(
        "map/",
        MapTemplateView.as_view(),
        name="map",
    ),
    # -------- program --------
    path(
        "program/<slug:program_slug>/detail/",
        ProgramDetailView.as_view(),
        name="program-detail",
    ),
    # -------- project paths --------
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/detail/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "program/<slug:program_slug>/project/",
        create_project,
        name="project"
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/update",
        update_project,
        name="update-project"
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/delete",
        delete_project,
        name="delete-project"
    ),
    path(
        "project/subproject/list/",
        SubProjectListView.as_view(),
        name="sub_project_list",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/sub_project/<slug:sub_project_slug>/delete/",
        delete_sub_project,
        name="sub-project-delete",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/sub_project/<slug:sub_project_slug>/update/",
        update_sub_project,
        name="sub-project-update",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/feedback/",
        create_feedback,
        name="feedback",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/detail/<slug:feedback_slug>/",
        edit_feedback,
        name="update-feedback",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/delete/<slug:feedback_slug>/",
        delete_feedback,
        name="delete-feedback",
    ),
    # -------- project fund --------
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/fund/",
        FundListAndCreateView.as_view(),
        name="fund-list",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/funds/<slug:fund_slug>",
        update_fund,
        name="fund-update",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/fund/<slug:fund_slug>/detail/",
        fund_detail,
        name="fund-detail",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/fund/<slug:fund_slug>/delete/",
        fund_delete,
        name="fund-delete",
    ),
    # -------- disbursement --------
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/funds/<slug:fund_slug>/disbursements/<slug:disbursement_slug>/delete/",
        delete_disbursement,
        name="disbursement-delete",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/funds/<slug:fund_slug>/disbursements/<slug:disbursement_slug>/update/",
        update_disbursement,
        name="disbursement-update",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/fund/<slug:fund_slug>/delete/",
        fund_delete,
        name="fund-delete",
    ),
    # -------- beneficiary --------
    # -------- training ------------
    path(
        "training/list/",
        TrainingListView.as_view(),
        name="training-list",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/training/list/",
        TrainingListView.as_view(),
        name="training-list",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/training/<slug:training_entry_slug>/training/delete/",
        training_delete,
        name="training-delete",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/training/<slug:training_entry_slug>/training/fetch/",
        training_fetch,
        name="training-fetch",
    ),
]
