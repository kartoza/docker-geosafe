# coding=utf-8
import os
from distutils.util import strtobool

import djcelery
from kombu import Queue
from celery.schedules import crontab

__author__ = 'Rizky Maulana Nugraha <lana.pcfre@gmail.com>'


def update_settings(settings):
    """Update settings file for geosafe."""
    settings.INSTALLED_APPS += ("geosafe", )
    settings.INSTALLED_APPS = list(settings.INSTALLED_APPS)

    # Make priority for geosafe templates
    template_dirs = list(settings.TEMPLATES[0]['DIRS'])
    template_dirs.insert(0, '/usr/src/geosafe/templates')

    settings.TEMPLATES[0]['DIRS'] = template_dirs
    settings.STATICFILES_DIRS += (
        '/usr/src/geosafe/static',
    )


    # Geosafe settings
    # App specific
    # Geosafe - Celery settings

    # Pick the correct broker for relaying commands to InaSAFE Headless
    settings.BROKER_URL = os.environ['BROKER_URL']
    settings.CELERY_RESULT_BACKEND = settings.BROKER_URL

    # Specific celery settings. Can be modified accordingly or leave as
    # default
    settings.CELERY_ALWAYS_EAGER = os.environ.get(
        'CELERY_ALWAYS_EAGER', False)
    if isinstance(settings.CELERY_ALWAYS_EAGER, str):
        settings.CELERY_ALWAYS_EAGER = strtobool(settings.CELERY_ALWAYS_EAGER)
    settings.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    settings.CELERY_IGNORE_RESULT = False
    settings.CELERY_SEND_EVENTS = True
    settings.CELERY_TASK_RESULT_EXPIRES = 24 * 3600
    settings.CELERY_DISABLE_RATE_LIMITS = True
    settings.CELERY_DEFAULT_QUEUE = "default"
    settings.CELERY_DEFAULT_EXCHANGE = "default"
    settings.CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
    settings.CELERY_DEFAULT_ROUTING_KEY = "default"
    settings.CELERY_CREATE_MISSING_QUEUES = True
    settings.CELERYD_CONCURRENCY = 1
    settings.CELERYD_PREFETCH_MULTIPLIER = 1

    # Defining Celery queue to avoid clash between tasks. Leave as default
    settings.CELERY_QUEUES = [
        Queue('default', routing_key='default'),
        Queue('cleanup', routing_key='cleanup'),
        Queue('update', routing_key='update'),
        Queue('email', routing_key='email'),
        Queue('inasafe-headless', routing_key='inasafe-headless'),
        Queue('geosafe', routing_key='geosafe'),
    ]

    # Schedule for periodic tasks
    settings.CELERYBEAT_SCHEDULE = {
        # executes every night at 0:0 AM
        'clean-impact-nightly': {
            'task': 'geosafe.tasks.analysis.clean_impact_result',
            'schedule': crontab(hour='0', minute='0')
        }
    }

    djcelery.setup_loader()

    # base url used to resolve layer files accessed by InaSAFE Headless
    settings.GEONODE_BASE_URL = os.environ.get(
        'GEONODE_BASE_URL', settings.SITEURL)
