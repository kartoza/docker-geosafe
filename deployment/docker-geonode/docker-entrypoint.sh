#!/usr/bin/env bash

set -e

echo "Number of arguments $#"

/usr/local/bin/invoke update >> /usr/src/app/invoke.log

source $HOME/.override_env

echo DATABASE_URL=$DATABASE_URL
echo GEODATABASE_URL=$GEODATABASE_URL
echo SITEURL=$SITEURL
echo ALLOWED_HOSTS=$ALLOWED_HOSTS
echo GEOSERVER_PUBLIC_LOCATION=$GEOSERVER_PUBLIC_LOCATION

/usr/local/bin/invoke waitfordbs >> /usr/src/app/invoke.log

echo "waitfordbs task done"

/usr/local/bin/invoke migrations >> /usr/src/app/invoke.log
echo "migrations task done"
/usr/local/bin/invoke prepare >> /usr/src/app/invoke.log
echo "prepare task done"
/usr/local/bin/invoke fixtures >> /usr/src/app/invoke.log
echo "fixture task done"

python manage.py collectstatic --noinput -i geoexplorer >> /usr/src/app/invoke.log
echo "collectstatic done"

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
exec "$@"
