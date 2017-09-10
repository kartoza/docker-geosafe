#!/usr/bin/env bash

# Run database migrations
echo "Run database migrations"
./manage.py makemigrations --noinput --merge
paver sync

# Run collectstatic
echo "Run collectstatic"
./manage.py collectstatic --noinput

# Apply permissions
echo "Apply permissions for QGIS Server"
chmod 777 geonode/qgis_layer
chmod 777 geonode/qgis_tiles

if [ "$DEBUG" == "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
	uwsgi --ini /uwsgi.conf
fi
