# coding=utf-8
from __future__ import absolute_import

from django.conf.urls import patterns, include

from geonode.urls import *

__author__ = 'Rizky Maulana Nugraha <lana.pcfre@gmail.com>'
__date__ = '8/25/16'

pattern_lists = [
    '',
]

if 'geosafe' in settings.INSTALLED_APPS:
    pattern_lists.append(
        (r'^geosafe/', include('geosafe.urls', namespace="geosafe")))

if pattern_lists:
    urlpatterns += patterns(*pattern_lists)
