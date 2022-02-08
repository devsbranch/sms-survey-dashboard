# -*- coding: utf-8 -*-
"""Settings for when running under docker in development mode."""
from .dev import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ['*',
                 u'0.0.0.0']

ADMINS = ()

# Set debug to True for development
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'cache:11211',
    }
}

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