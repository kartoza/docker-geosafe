#!/usr/bin/env bash

set -e

# Apply permissions
echo "Apply permissions for QGIS Server"
mkdir -p geonode/qgis_layer
chmod 777 geonode/qgis_layer
mkdir -p geonode/qgis_tiles
chmod 777 geonode/qgis_tiles

echo "Number of arguments $#"

/usr/local/bin/invoke update >> /usr/src/app/invoke.log

source $HOME/.override_env

echo DATABASE_URL=$DATABASE_URL
echo GEODATABASE_URL=$GEODATABASE_URL
echo SITEURL=$SITEURL
echo ALLOWED_HOSTS=$ALLOWED_HOSTS
echo GEOSERVER_PUBLIC_LOCATION=$GEOSERVER_PUBLIC_LOCATION
echo STATIC_ROOT=$STATIC_ROOT
echo MEDIA_ROOT=$MEDIA_ROOT

/usr/local/bin/invoke waitfordbs

echo "waitfordbs task done"

/usr/local/bin/invoke migrations
echo "migrations task done"

echo "Lock file: $MEDIA_ROOT/geonode_init.lock"

if [ ! -e "$MEDIA_ROOT/geonode_init.lock" ]; then

	echo "Lock file doesn't exists, perform initializations"

	python manage.py collectstatic --noinput --clear
	echo "collectstatic done"

	/usr/local/bin/invoke prepare
	echo "prepare task done"

	/usr/local/bin/invoke fixtures
	echo "fixture task done"

	echo "Initialize geonode_init.lock"
	date > $MEDIA_ROOT/geonode_init.lock
else
	echo "Lock file exists. Skip initializations"
fi

if [ $# -eq 1 ]; then
	case $1 in
		# Debug mode, run manage.py in debug mode
		[Dd][Ee][Bb][Uu][Gg])
			echo "Running in debug mode. Run Django Server"
			exec python manage.py runserver 0.0.0.0:8000
			exit
			;;
		# Production mode, run using uwsgi
		[Pp][Rr][Oo][Dd])
			echo "Running in prod mode. Run uWSGI"
			exec uwsgi --ini /uwsgi.conf &
			# Put trap
			trap "echo \"Sending SIGTERM to uWSGI\"; uwsgi --stop /tmp/django.pid; killall -s SIGTERM tail" SIGTERM
			touch /var/log/uwsgi-errors.log
			echo "Displaying error logs."
			tail -f /var/log/uwsgi-errors.log
			exit
			;;
	esac
fi

# Run as bash entrypoint
exec "$@"
