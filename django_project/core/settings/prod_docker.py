
"""Configuration for production server"""
# noinspection PyUnresolvedReferences
from .prod import *  # noqa
import os

DEBUG = True # just to quickly get dev work going until ready for prod rollout

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Alison Mukoma', 'mukoamlison@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USERNAME'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}


# See fig.yml file for postfix container definition
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
EMAIL_HOST = 'smtp'
# Port for sending e-mail.
EMAIL_PORT = 25
# SMTP authentication information for EMAIL_HOST.
# See fig.yml for where these are defined
EMAIL_HOST_USER = 'noreply@digiprophets.com'
EMAIL_HOST_PASSWORD = 'docker'
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = '[PPCR-TRALARD]'

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'beneficiary.search_backends.fuzzy_elastic_search_engine'
#                   '.FuzzyElasticSearchEngine',
#         'URL': 'http://%s:9200/' % os.environ['HAYSTACK_HOST'],
#         'INDEX_NAME': 'haystack',
#     },
# }

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("CELERY_BROKER_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

SELECT2_CACHE_BACKEND = "select2"
