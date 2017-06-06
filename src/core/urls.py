# coding=utf-8
from __future__ import absolute_import
from django.conf import settings
from django.conf.urls import include, patterns

__author__ = 'Rizky Maulana Nugraha <lana.pcfre@gmail.com>'
__date__ = '8/25/16'


pattern_lists = [
    '',
    # geonode urls
    (r'', include('geonode.urls')),
]

if 'geosafe' in settings.INSTALLED_APPS:
    pattern_lists.append(
        (r'^geosafe/', include('geosafe.urls', namespace="geosafe")))

urlpatterns = patterns(*pattern_lists)
