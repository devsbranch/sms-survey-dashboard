# coding=utf-8
__author__ = 'Alison Mukoma <mukomalison@gmail.com>Alison '
__date__ = '15/12/2021'

from rolepermissions.roles import AbstractUserRole


class ProjectManager(AbstractUserRole):
    role_name = 'project_manager'
    available_permissions = {
        'permission_1': True,
        'permission_2': True
    }


class Funder(AbstractUserRole):
    role_name = 'funder'
    available_permissions = {
        'permission_1': True,
        'permission_3': True,
    }

class ProjectSupervisor(AbstractUserRole):
    role_name = 'project_supervisor'
    available_permissions = {
        'permission_1': True,
        'permission_3': True,
    }

class BenficiaryRepresentative(AbstractUserRole):
    role_name = 'benficiary_epresentative'
    available_permissions = {
        'permission_1': True,
        'permission_3': True,
    }
