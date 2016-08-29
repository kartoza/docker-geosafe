#!/usr/bin/env bash

cp -n /celeryconfig.py /usr/src/geosafe/tasks/headless/celeryconfig.py

python manage.py runserver 0.0.0.0:8000
