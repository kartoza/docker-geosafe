# coding=utf-8
import os
import sys
import importlib
from ast import literal_eval

from celery.schedules import crontab
from kombu import Queue

__author__ = 'Rizky Maulana Nugraha <lana.pcfre@gmail.com>'


settings_file = os.environ.get(
    'DJANGO_SETTINGS_MODULE', 'geonode.settings')
if settings_file not in sys.modules:
    current_settings = importlib.import_module(settings_file)
    sys.modules[settings_file] = current_settings
else:
    current_settings = sys.modules[settings_file]

locals().update({
    k: getattr(current_settings, k)
    for k in dir(current_settings) if not k.startswith('_')
})

# Settings for GeoSAFE
DATABASES["default"]["ENGINE"] = \
        'django.contrib.gis.db.backends.postgis'

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append('geosafe')

# Make priority for geosafe templates
template_dirs = list(TEMPLATES[0]['DIRS'])
template_dirs.insert(0, '/usr/src/geosafe/templates')

TEMPLATES[0]['DIRS'] = template_dirs

# Include GeoSAFE locale path
LOCALE_PATHS = list(LOCALE_PATHS)
LOCALE_PATHS.insert(0, '/usr/src/geosafe/locale')

# Geosafe settings
# App specific
# Geosafe - Celery settings

# Pick the correct broker for relaying commands to InaSAFE Headless
BROKER_URL = os.environ['BROKER_URL']
CELERY_RESULT_BACKEND = BROKER_URL

# Specific celery  Can be modified accordingly or leave as
# default
CELERY_TASK_ALWAYS_EAGER = literal_eval(os.environ.get(
    'CELERY_TASK_ALWAYS_EAGER', 'False'))
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_IGNORE_RESULT = False
CELERY_SEND_EVENTS = True
CELERY_TASK_RESULT_EXPIRES = 24 * 3600
CELERY_DISABLE_RATE_LIMITS = True
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"
CELERY_CREATE_MISSING_QUEUES = True
CELERYD_CONCURRENCY = 1
CELERYD_PREFETCH_MULTIPLIER = 1

# Celery config
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = {'pickle'}
CELERY_RESULT_SERIALIZER = 'pickle'

# Defining Celery queue to avoid clash between tasks. Leave as default
CELERY_QUEUES = [
    Queue('default', routing_key='default'),
    Queue('cleanup', routing_key='cleanup'),
    Queue('update', routing_key='update'),
    Queue('email', routing_key='email'),
    Queue('inasafe-headless', routing_key='inasafe-headless'),
    Queue('geosafe', routing_key='geosafe'),
]

# Schedule for periodic tasks
CELERYBEAT_SCHEDULE = {
    # executes every night at 0:0 AM
    'clean-impact-nightly': {
        'task': 'geosafe.tasks.analysis.clean_impact_result',
        'schedule': crontab(hour='0', minute='0')
    }
}

# Specific settings for GeoSAFE

# Opt-in to use layerfile direct disk access for InaSAFE Headless Celery
# workers instead of Http
USE_LAYER_FILE_ACCESS = literal_eval(os.environ.get(
    'USE_LAYER_FILE_ACCESS', 'True'))

INASAFE_LAYER_DIRECTORY = os.environ.get(
    'INASAFE_LAYER_DIRECTORY', '/home/geosafe/media/')

INASAFE_LAYER_DIRECTORY_BASE_PATH = os.environ.get(
    'INASAFE_LAYER_DIRECTORY_BASE_PATH', '/usr/src/app/geonode/qgis_layer/')

GEOSAFE_IMPACT_OUTPUT_DIRECTORY = os.environ.get(
    'GEOSAFE_IMPACT_OUTPUT_DIRECTORY', '/home/geosafe/impact_layers/')

INASAFE_IMPACT_BASE_URL = os.environ.get(
    'INASAFE_IMPACT_BASE_URL', '/output/')

# Opt-in to use layerfile http access for InaSAFE Headless Celery
# workers instead of disk access
USE_LAYER_HTTP_ACCESS = literal_eval(os.environ.get(
    'USE_LAYER_HTTP_ACCESS', 'False'))

# base url used to resolve layer files accessed by InaSAFE Headless
GEONODE_BASE_URL = os.environ.get(
    'GEONODE_BASE_URL', SITEURL)

# Analysis Run Time Limit (in seconds)
# Task will exit if exceeded this hard limit
INASAFE_ANALYSIS_RUN_TIME_LIMIT = literal_eval(os.environ.get(
    'INASAFE_ANALYSIS_RUN_TIME_LIMIT', '600'))

# Analysis area limit (in meter squares)
# Create analysis will display warning if analysis extent
# exceeded this limit. User will be able to continue analysis
# with warning that analysis will might take a long time.
INASAFE_ANALYSIS_AREA_LIMIT = literal_eval(os.environ.get(
    'INASAFE_ANALYSIS_AREA_LIMIT', '1000000000'))

# QGIS report template settings
# You can use this if you have custom template file
# LOCALIZED_QGIS_REPORT_TEMPLATE = {
#     'en': os.path.join(
#         template_dirs[0], 'geosafe', 'qgis_templates', 'en', 'map-report.qpt')
# }
