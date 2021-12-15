# coding=utf-8
__author__ = 'Alison Mukoma <mukomalison@gmail.com>Alison '
__date__ = '15/12/2021'

from rolepermissions.roles import AbstractUserRole


class ReportManager(AbstractUserRole):
    available_permissions = {
        'can_view_my_project_report': True,
        'can_edit_my_project_report': True,
        'can_export_project_report': True,
    }

class DataAnalyst(AbstractUserRole):
    available_permissions = {
        'can_view_my_project_data': True,
        'can_edit_my_project_data': True,
        'can_delete_my_project_data': True,
    }


class User(AbstractUserRole):
    available_permissions = {}

class ProjectManager(AbstractUserRole):
    available_permissions = {
        'can_view_my_project': True,
        'can_edit_my_project': True,
        'can_delete_my_project': True,
        'can_edit_funding_data': True,
        'can_assign_project_supervisor': True,
    }


class Funder(AbstractUserRole):
    available_permissions = {
        'can_create_funding_data': True,
        'can_edit_funding_data': True,
        'can_delete_funding_data': True,
        'can_assign_project_manager': True,
    }

class ProjectSupervisor(AbstractUserRole):
    available_permissions = {
        'can_view_my_project_beneficiary': True,
        'can_edit_my_project_beneficiary': True,
    }

class BenficiarySubProjectRepresentative(AbstractUserRole):
    available_permissions = {
        'can_view_my_sub_project_data': True,
        'can_edit_my_sub_project_data': True,
    }
