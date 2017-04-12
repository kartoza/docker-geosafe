# coding=utf-8
from __future__ import absolute_import
from django.conf.urls import include, patterns, url

__author__ = 'Rizky Maulana Nugraha <lana.pcfre@gmail.com>'
__date__ = '8/25/16'


urlpatterns = patterns(
    '',
    # geonode urls
    (r'', include('geonode.urls')),
    # geosafe urls
    (r'', include('geosafe.urls', namespace="geosafe")),
    # qgis_server urls
    (r'', include('geonode.qgis_server.urls', namespace="qgis_server")),
)
