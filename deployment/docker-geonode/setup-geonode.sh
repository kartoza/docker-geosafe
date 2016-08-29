#!/usr/bin/env bash
service apache2 restart
python manage.py runserver 0.0.0.0:8000
