# -*- coding: utf-8
from django.apps import AppConfig


class TralardConfig(AppConfig):
    name = 'tralard'

    def ready(self):
        import tralard.signals  # noqa F401