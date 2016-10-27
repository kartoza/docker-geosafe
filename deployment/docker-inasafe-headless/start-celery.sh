#!/usr/bin/env bash

cp -n /celeryconfig.py /home/src/inasafe/headless/celeryconfig.py

start-stop-daemon --start -b -x /usr/bin/Xvfb :99
source run-env-linux.sh /usr

if [ $# -eq 1 ] && [ $1 = "dev" ]; then
    /usr/sbin/sshd -D
elif [ $# -eq 2 ] && [ $1 = "prod" ] && [ $2 = "inasafe-headless" ]; then
    celery -A headless.celery_app worker -l info -Q inasafe-headless -n inasafe-headless.%h
elif [ $# -eq 2 ] && [ $1 = "prod" ] && [ $2 = "inasafe-headless-analysis" ]; then
    celery -A headless.celery_app worker -l info -Q inasafe-headless-analysis -n inasafe-headless-analysis.%h
fi