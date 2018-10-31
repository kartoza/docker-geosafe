#!/usr/bin/env bash

set -e

install-theme-app.sh

python manage.py compilemessages >> /usr/src/app/invoke.log
echo "compilemessages done"

# Run as bash entrypoint
exec "$@"
