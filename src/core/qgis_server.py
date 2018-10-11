# coding=utf-8
import os
import sys
import importlib
from ast import literal_eval

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

# Settings for QGIS Server

_qgis_server_apps_package = "geonode.qgis_server"

GEONODE_APPS = list(GEONODE_APPS)
if _qgis_server_apps_package not in GEONODE_APPS:

    GEONODE_APPS += ("geonode.qgis_server", )

INSTALLED_APPS = list(INSTALLED_APPS)
if _qgis_server_apps_package not in INSTALLED_APPS:
    INSTALLED_APPS += (
        "geonode.qgis_server", )

# Delete Geoserver settings
# Not using GeoFence if using QGIS Server Backend
GEOFENCE_SECURITY_ENABLED = False

USE_GEOSERVER = False

INSTALLED_APPS.remove("geonode.geoserver")
GEONODE_APPS.remove("geonode.geoserver")

if hasattr(current_settings, 'PUBLIC_GEOSERVER') and \
        PUBLIC_GEOSERVER in MAP_BASELAYERS:
    MAP_BASELAYERS.remove(PUBLIC_GEOSERVER)
    del PUBLIC_GEOSERVER

if hasattr(current_settings, 'LOCAL_GEOSERVER') and \
        LOCAL_GEOSERVER in MAP_BASELAYERS:
    MAP_BASELAYERS.remove(LOCAL_GEOSERVER)
    del LOCAL_GEOSERVER

geoserver_context_processor = 'geonode.geoserver.context_processors.geoserver_urls'
if geoserver_context_processor in TEMPLATES[0]['OPTIONS']['context_processors']:
    TEMPLATES[0]['OPTIONS']['context_processors'].remove(geoserver_context_processor)

qgis_server_context_processor = 'geonode.qgis_server.context_processors.qgis_server_urls'
TEMPLATES[0]['OPTIONS']['context_processors'].append(qgis_server_context_processor)

# Celery config
CELERY_ALWAYS_EAGER = literal_eval(os.environ.get(
    'CELERY_ALWAYS_EAGER', 'False'))
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = {'pickle'}
CELERY_RESULT_SERIALIZER = 'pickle'

# Leaflet config
GEONODE_CLIENT_LAYER_PREVIEW_LIBRARY = 'leaflet'
GEONODE_CLIENT_HOOKSET = 'geonode.client.hooksets.LeafletHookSet'
if not hasattr(current_settings, 'LEAFLET_CONFIG'):
    LEAFLET_CONFIG = {
        'TILES': [
            # Map Quest
            ('Map Quest',
             'http://otile4.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
             'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> '
             '&mdash; Map data &copy; '
             '<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'),
        ],
        'PLUGINS': {
            'esri-leaflet': {
                'js': 'lib/js/esri-leaflet.js',
                'auto-include': True,
            },
            'leaflet-fullscreen': {
                'css': 'lib/css/leaflet.fullscreen.css',
                'js': 'lib/js/Leaflet.fullscreen.min.js',
                'auto-include': True,
            },
        },
        'SRID': 3857,
        'RESET_VIEW': False
    }

# QGIS Server as local OGC Server, wrapped by geonode itself.
OGC_URL_INSIDE = os.environ.get('OGC_URL_INSIDE', SITEURL)
OGC_SERVER = {
    'default': {
        'BACKEND': 'geonode.qgis_server',
        'LOCATION': OGC_URL_INSIDE + 'qgis-server/',
        'PUBLIC_LOCATION': SITEURL + 'qgis-server/',
        'GEOFENCE_SECURITY_ENABLED': GEOFENCE_SECURITY_ENABLED,
        'LOG_FILE': ''
    }
}

# OGC (WMS/WFS/WCS) Server Settings
tiles_directory = os.path.join(PROJECT_ROOT, "qgis_tiles")
layer_directory = os.path.join(PROJECT_ROOT, "qgis_layer")
QGIS_SERVER_URL = os.environ.get(
    'QGIS_SERVER_URL', 'http://qgis-server/')
QGIS_SERVER_CONFIG = {
    'tiles_directory': tiles_directory,
    'tile_path': tiles_directory + '/%s/%s/%d/%d/%d.png',
    'legend_path': tiles_directory + '/%s/%s/legend.png',
    'thumbnail_path': tiles_directory + '/%s/thumbnail.png',
    'map_tile_path': os.path.join(
        tiles_directory, '%s', 'map_tiles', '%s', '%s', '%s', '%s.png'),
    'qgis_server_url': QGIS_SERVER_URL,
    'layer_directory': layer_directory
}

# Middleware classes
MIDDLEWARE_CLASSES += (
    'geonode.qgis_server.middleware.QGISServerLayerMiddleware',
)
