# coding=utf-8
from __future__ import absolute_import

import ast
import sys
import os

__author__ = 'Rizky Maulana Nugraha <lana.pcfre@gmail.com>'
__date__ = '8/25/16'


try:
    # import geonode settings
    from geonode.settings import *
    this_settings = sys.modules[__name__]
except ImportError:
    pass

try:
    # if using QGIS Server, import settings
    ogc_backend = os.environ.get('OGC_BACKEND', 'geonode.qgis_server')
    if ogc_backend == 'geonode.qgis_server':
        from core.qgis_server import update_settings
        update_settings(this_settings)
except ImportError:
    pass

try:
    # if using Geosafe, import settings
    use_geosafe = os.environ.get('USE_GEOSAFE', 'True')
    use_geosafe = ast.literal_eval(use_geosafe)
    if use_geosafe:
        from core.geosafe import update_settings
        update_settings(this_settings)
except ImportError:
    pass

# Loggers
if DEBUG:
    LOGGING["handlers"]["console"]["level"] = "DEBUG"

    LOGGING["loggers"]["geonode"] = {
        "handlers": ["console"],
        "level": "DEBUG",
    }
    LOGGING["loggers"]["geosafe"] = {
        "handlers": ["console"],
        "level": "DEBUG",
    }

    INSTALLED_APPS = ['test_without_migrations'] + INSTALLED_APPS

    # Specify test database name
    # This allow a separate database instance when running
    DATABASES['default']['TEST'] = {
        'NAME': 'unittests'
    }

    # Redefine databases entry for unittests
    # If this flag is set to true, then it is a celery worker instance
    # for Django unittests
    CELERY_TESTING_WORKER = ast.literal_eval(os.environ.get(
        'CELERY_TESTING_WORKER', 'False'))

    if CELERY_TESTING_WORKER:
        # Celery can't detect if it is using a test database mode or not
        # So, for unittesting we specify test database for celery to use
        DATABASES['default']['NAME'] = 'unittests'

try:
    # convert to list
    allowed_hosts = os.environ['ALLOWED_HOSTS']
    ALLOWED_HOSTS = ast.literal_eval(allowed_hosts)
except:
    pass

# Used when running test in development mode
TESTING = sys.argv[1:2] == ['test'] or os.environ.get('TESTING')
