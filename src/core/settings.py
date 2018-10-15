# coding=utf-8
from __future__ import absolute_import

import importlib
import ast
import sys
import os
from distutils.util import strtobool

__author__ = 'Rizky Maulana Nugraha <lana.pcfre@gmail.com>'
__date__ = '8/25/16'


def update_settings_from(settings_name):
    """This method will try to update settings.

    It works as follows.

    The way GeoNode made as platform will let us to cascade different
    settings for each django app that uses GeoNode as a platform.

    We just need to load each settings and updated current locals modules.

    Let's say, the sites root settings is located (and described) in
    DJANGO_SETTINGS_MODULE

    This is the current file 'core.settings'

    This file will dictate which settings will load first and which to
    override form.

    Usually, 'geonode.settings' needs to be loaded first to include some
    basic settings. Then we need to override some settings based on the app
    we used. So we do

    update_settings_from(settings_name, current_module)

    To override settings in this module.

    By the design of Django, all needed settings starts with capital letter
    all Uppercase. So we exclude any files prefixed by _ since it is only of
    local module's concern.

    :param settings_name: The settings name in the format of python modules
        e.g. core.settings
    :type settings_name: basestring

    :return: will return current module
    :rtype: module
    """
    app_settings = importlib.import_module(settings_name)
    return {
        k: getattr(app_settings, k)
        for k in dir(app_settings) if not k.startswith('_')
    }


try:
    # import geonode settings
    geonode_settings = update_settings_from('geonode.settings')
    locals().update(geonode_settings)
    this_settings = sys.modules['geonode.settings']
except ImportError:
    pass

# Email settings
if EMAIL_ENABLE:
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp')
    EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'noreply')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'docker')
    EMAIL_USE_TLS = strtobool(os.environ.get('EMAIL_USE_TLS', 'False'))
    DEFAULT_FROM_EMAIL = os.environ.get(
        'DEFAULT_FROM_EMAIL', 'GeoNode <no-reply@{0}>'.format(SITEURL))
else:
    EMAIL_BACKEND = os.getenv('DJANGO_EMAIL_BACKEND',
                              default='django.core.mail.backends.console.EmailBackend')

try:
    # if using QGIS Server, import settings
    ogc_backend = os.environ.get('OGC_BACKEND', 'geonode.qgis_server')
    if ogc_backend == 'geonode.qgis_server':
        qgis_server_settings = update_settings_from('core.qgis_server')
        locals().update(qgis_server_settings)
except ImportError:
    pass

try:
    # if using Geosafe, import settings
    use_geosafe = os.environ.get('USE_GEOSAFE', 'True')
    use_geosafe = ast.literal_eval(use_geosafe)
    if use_geosafe:
        geosafe_settings = update_settings_from('core.geosafe')
        locals().update(geosafe_settings)
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
    theme_settings = update_settings_from(
        '{app_name}.settings'.format(app_name=THEME_APP_NAME))
    locals().update(theme_settings)

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

    INSTALLED_APPS = list(INSTALLED_APPS)
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
