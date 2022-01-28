# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from tralard.views.training import (
    training_update,
    training_delete,
    TrainingListView,
    template_testing,
)
from tralard.views.beneficiary import (
    beneficiary_detail,
    beneficiary_update,
    beneficiary_delete,
    BeneficiaryOrgListView,
)
from tralard.views.fund import (
    fund_detail,
    update_fund,
    fund_delete,
    delete_disbursement,
    update_disbursement,
    FundListAndCreateView,
    get_disbursement_expenditures,
)
from tralard.views.project import (
    edit_feedback,
    project_update,
    project_create,
    project_delete,
    create_feedback,
    delete_feedback,
    ProjectDetailView,
    delete_sub_project,
    update_sub_project,
)
from tralard.views.sub_project import (
    poll_state,
    indicator_report,
    SubProjectDetailView,
    fund_approval_view,
    subproject_fund_delete,
    subproject_fund_detail,
    update_sub_project_fund,
    SubProjectTrainingListView,
    sub_project_training_delete,
    sub_project_training_update,
    SubProjectFundListAndCreateView,
    SubProjectBeneficiaryOrgListView,
    subproject_fund_disbursement_create,
)
from tralard.views.map import MapTemplateView
from tralard.views.dashboard import HomeTemplateView
from tralard.views.profile import user_profile_update
from tralard.views.sub_project import (
    subproject_disbursement_expenditure_create,
    sub_project_update,
)
from tralard.views.program import ProgramDetailView, preview_indicator_document

app_name = "tralard"
urlpatterns = [
    path(
        "test/",
        template_testing,
        name="test",
    ),
    # -------- dashboard --------
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
    # -------- Indicator report download --------
    path(
        "report/<slug:program_slug>/indicators_report/preview_report/",
        preview_indicator_document,
        name="preview_indicator_report",
    ),
    path(
        "report/indicators_report/",
        indicator_report,
        name="indicators_report_download",
    ),
    path(
        "report/indicators_report/<str:task_id>",
        poll_state,
        name="poll_state",
    ),
    # -------- Program -----------
    path(
        "program/<slug:program_slug>/detail/",
        ProgramDetailView.as_view(),
        name="program-detail",
    ),
    # -------- user profile --------
    path(
        "user/profile/update/",
        user_profile_update,
        name="profile-update",
    ),
    # -------- project paths --------
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/detail/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path("program/<slug:program_slug>/project/", project_create, name="project"),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/update",
        project_update,
        name="project-update",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/delete",
        project_delete,
        name="project-delete",
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
        "program/<slug:program_slug>/project/<slug:project_slug>/fund/<slug:fund_slug>/disbursement/<slug:disbursement_slug>/expenditure/",
        get_disbursement_expenditures,
        name="disbursement-expenditure",
    ),
    # -------- project beneficiary --------
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/beneficiary/list/",
        BeneficiaryOrgListView.as_view(),
        name="beneficiary-list",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/beneficiary/<slug:beneficiary_slug>/update/",
        beneficiary_update,
        name="beneficiary-update",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/beneficiary/<slug:beneficiary_slug>/delete/",
        beneficiary_delete,
        name="beneficiary-delete",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/beneficiary/<slug:beneficiary_slug>/detail/",
        beneficiary_detail,
        name="beneficiary-detail",
    ),
    # -------- sub project beneficiary --------
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/beneficiary/",
        SubProjectBeneficiaryOrgListView.as_view(),
        name="subproject-beneficiary",
    ),
    # -------- training ------------
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
        "program/<slug:program_slug>/project/<slug:project_slug>/training/<slug:training_entry_slug>/update/",
        training_update,
        name="training-update",
    ),
    # -------- SubProject --------
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/manage/",
        SubProjectDetailView.as_view(),
        name="subproject-manage",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/training/list/",
        SubProjectTrainingListView.as_view(),
        name="subproject-training",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/training/<slug:training_entry_slug>/delete/",
        sub_project_training_delete,
        name="subproject-training-delete",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/training/<slug:training_entry_slug>/update/",
        sub_project_training_update,
        name="subproject-training-update",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/manage/fund/",
        SubProjectFundListAndCreateView.as_view(),
        name="subproject-fund-list",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/manage/fund/<slug:fund_slug>/detail/",
        subproject_fund_detail,
        name="subproject-fund-detail",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/manage/fund/<slug:fund_slug>/",
        update_sub_project_fund,
        name="subproject-fund-update",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/manage/fund/<slug:fund_slug>/delete/",
        subproject_fund_delete,
        name="subproject-fund-delete",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/manage/fund/<slug:fund_slug>/disbursement/",
        subproject_fund_disbursement_create,
        name="subproject-fund-disbursement-create",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/manage/fund/<slug:fund_slug>/disbursement/<slug:disbursement_slug>/",
        subproject_disbursement_expenditure_create,
        name="subproject-fund-disbursement-expenditure-create",
    ),
    path(
        "program/<slug:program_slug>/subproject/<slug:subproject_slug>/update/",
        sub_project_update,
        name="subproject-update",
    ),
    path(
        "program/<slug:program_slug>/project/<slug:project_slug>/subproject/<slug:subproject_slug>/manage/fund/<slug:fund_slug>/approve/",
        fund_approval_view,
        name="subproject-fund-approval"
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
