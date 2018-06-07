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

echo "Number of arguments $#"

if [ $# -eq 1 ]; then
	case $1 in
		# Dev mode, allow ssh
		[Dd][Ee][Vv])
			echo "Running in dev mode. Allowing SSH"
			exec /usr/sbin/sshd -D
			exit
			;;
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
exec $@
