# coding=utf-8
__author__ = "Alison Mukoma <mukomalison@gmail.com>Alison "
__date__ = "15/12/2021"


from rolepermissions.roles import AbstractUserRole


class ReportManager(AbstractUserRole):
    available_permissions = {
        "can_view_subcomponent_report": True,
        "can_edit_subcomponent_report": True,
        "can_export_subcomponent_report": True,
    }


class DataAnalyst(AbstractUserRole):
    available_permissions = {
        "can_view_subcomponent_data": True,
        "can_edit_subcomponent_data": True,
        "can_delete_subcomponent_data": True,
    }


class User(AbstractUserRole):
    available_permissions = {}


class ProjectManager(AbstractUserRole):
    role_name = "project_manager"
    available_permissions = {
        "can_create_project":True,
    }


class SubComponentManager(AbstractUserRole):
    role_name = "subcomponent_manager"
    available_permissions = {
        "can_create_subcomponent": True,
        "can_view_subcomponent": True,
        "can_edit_subcomponent": True,
        "can_delete_subcomponent": True,
        "can_assign_subcomponent_supervisor": True,
        "can_edit_funding_data": True,
    }


class Funder(AbstractUserRole):
    role_name = "funder"
    available_permissions = {
        "can_create_funding_data": True,
        "can_edit_funding_data": True,
        "can_delete_funding_data": True,
        "can_view_funding_data": True,
        "can_assign_subcomponent_manager": True,
    }


class SubComponentSupervisor(AbstractUserRole):
    available_permissions = {
        "can_view_subcomponent_beneficiary": True,
        "can_edit_subcomponent_beneficiary": True,
    }


class BenficiarySubProjectRepresentative(AbstractUserRole):
    available_permissions = {
        "can_view_sub_project_data": True,
        "can_edit_sub_project_data": True,
    }


class TrainingManager(AbstractUserRole):
    role_name = "training_manager"
    available_permissions = {
        "can_view_subcomponent_training": True,
        "can_edit_training_subcomponent": True,
        "can_view_training_sub_project": True,
        "can_edit_training_sub_project": True,
    }


class CertificationManager(AbstractUserRole):
    role_name = "certification_manager"
    available_permissions = {
        "can_view_subcomponent": True,
        "can_edit_subcomponent": True,
        "can_delete_subcomponent": True,
    }
