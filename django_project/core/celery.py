from __future__ import absolute_import

import os
from django.conf import settings

from celery import Celery

app = Celery('core')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev_docker")


app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()
