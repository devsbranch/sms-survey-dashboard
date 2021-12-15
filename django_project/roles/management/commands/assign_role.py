# coding=utf-8
__author__ = 'Alison Mukoma <mukomalison@gmail.com>Alison '
__date__ = '15/12/2021'

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rolepermissions.roles import assign_role

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """ Assign role to user.
    """
    args = '<message>'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('role')

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']
        if username and role:
            try:
                user = User.objects.get(username=username)
                assign_role(user, role)
                print('success')
            except User.DoesNotExist:
                print('user does not found')
