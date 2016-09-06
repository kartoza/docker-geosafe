#!/usr/bin/env bash

cp -n /celeryconfig.py /usr/src/geosafe/tasks/headless/celeryconfig.py

if [ $# -eq 1 ] && [ $1 = "dev" ]; then
    /usr/sbin/sshd -D
else
    python manage.py runserver 0.0.0.0:8000
fi
