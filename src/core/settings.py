# coding=utf-8
from __future__ import absolute_import

import importlib
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

# Custom theme settings
USE_THEME_APP = ast.literal_eval(
    os.environ.get('USE_THEME_APP', 'False'))

if USE_THEME_APP:

    THEME_APP_NAME = os.environ.get('THEME_APP_NAME', None)
    THEME_APP_PATH = os.environ.get('THEME_APP_PATH', None)

    INSTALLED_APPS = list(INSTALLED_APPS)
    INSTALLED_APPS.append(THEME_APP_NAME)

    # Prioritize custom translations
    if THEME_APP_PATH:
        LOCALE_PATHS = list(LOCALE_PATHS)
        LOCALE_PATHS.insert(
            0, os.path.join(
                THEME_APP_PATH,
                THEME_APP_NAME,
                'locale'))

        # Prioritize custom theme
        template_dirs = list(TEMPLATES[0]['DIRS'])
        template_dirs.insert(
            0, os.path.join(
                THEME_APP_PATH,
                THEME_APP_NAME,
                'templates'))

        TEMPLATES[0]['DIRS'] = template_dirs

    # Import app settings
    importlib.import_module(
        '{app_name}.settings'.format(app_name=THEME_APP_NAME))

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
