SHELL := /bin/bash
PROJECT_ID := geonode-docker
DELAY = 5

# ----------------------------------------------------------------------------
#    P R O D U C T I O N     C O M M A N D S
# ----------------------------------------------------------------------------

up:
	# bring up the services
	@docker-compose -p $(PROJECT_ID) up -d

default: deploy

ansible-check:
	@echo "Check ansible command"
	@ansible -i ansible/development/hosts all -m ping
	@ansible-playbook -i ansible/development/hosts ansible/development/site.yml --list-tasks --list-hosts $(ANSIBLE_ARGS)

setup-ansible:
	@echo "Setup configurations using ansible"
	@ansible-playbook -i ansible/development/hosts ansible/development/site.yml $(ANSIBLE_ARGS)

build-geonode-core:
	@echo "Building core GeoNode container as image base"
	@cd ../src/geonode; docker pull geonode/django:latest; docker-compose build django

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) build

default-scale:
	@docker-compose -p $(PROJECT_ID) scale qgis-server=1 qgis-server-backend=1 celery=1 inasafe-headless=1 inasafe-headless-analysis=1

production-scale:
	@docker-compose -p $(PROJECT_ID) scale qgis-server=1 qgis-server-backend=4 celery=4 inasafe-headless=4 inasafe-headless-analysis=4

sync: up
	@docker-compose -p $(PROJECT_ID) exec django django-admin.py makemigrations --noinput --merge
	@docker-compose -p $(PROJECT_ID) exec django paver sync

collectstatic: up
	@docker-compose -p $(PROJECT_ID) exec django django-admin.py collectstatic

reload:
	@docker-compose -p $(PROJECT_ID) exec django uwsgi --reload  /tmp/django.pid

restart-qgis-server:
	@docker kill geonodedocker_qgis-server_1
	@docker rm geonodedocker_qgis-server_1
	@docker-compose -p $(PROJECT_ID) up -d

restart-celery:
	@docker-compose -p $(PROJECT_ID) restart celery
	@docker-compose -p $(PROJECT_ID) restart inasafe-headless
	@docker-compose -p $(PROJECT_ID) restart inasafe-headless-analysis

shell:
	@docker-compose -p $(PROJECT_ID) exec django /bin/bash

status:
	@docker-compose -p $(PROJECT_ID) ps

dblogs:
	@docker-compose -p $(PROJECT_ID) logs -f --tail=30 postgis

geosafe-env:
	@docker-compose -p $(PROJECT_ID) exec django printenv

geosafe-celery-env:
	@docker-compose -p $(PROJECT_ID) exec celery printenv

inasafe-headless-env:
	@docker-compose -p $(PROJECT_ID) exec inasafe-headless /bin/bash -c "source run-env-linux.sh /usr; printenv"

qgis-server-backend-log:
	@docker-compose -p $(PROJECT_ID) logs -f --tail=50 qgis-server-backend

geosafe-log:
	@docker-compose -p $(PROJECT_ID) logs -f --tail=50 django

geosafe-celery-log:
	@docker-compose -p $(PROJECT_ID) logs -f --tail=50 celery

inasafe-headless-log:
	@docker-compose -p $(PROJECT_ID) logs -f --tail=50 inasafe-headless

inasafe-headless-analysis-log:
	@docker-compose -p $(PROJECT_ID) logs -f --tail=50 inasafe-headless-analysis

setup: build
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Setup in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run geonode /setup-geonode.sh
	@docker-compose -p $(PROJECT_ID) run inasafe-headless /setup-geonode.sh

wait:
	sleep $(DELAY)

logs:
	@docker-compose -p $(PROJECT_ID) logs --follow

down:
	@docker-compose -p $(PROJECT_ID) down

pull:
	@docker-compose -p $(PROJECT_ID) pull

smoketest: up
	@docker-compose -p $(PROJECT_ID) exec django python manage.py test geonode.tests.smoke --nocapture --detailed-errors --verbosity=1 --failfast

unittest: up
	@docker-compose -p $(PROJECT_ID) exec django python manage.py test geonode.people.tests geonode.base.tests geonode.layers.tests geonode.maps.tests geonode.proxy.tests geonode.security.tests geonode.social.tests geonode.catalogue.tests geonode.documents.tests geonode.api.tests geonode.groups.tests geonode.services.tests geonode.geoserver.tests geonode.upload.tests geonode.tasks.tests --noinput --failfast

geosafe-test:
	@docker-compose -p $(PROJECT_ID) exec django coverage run --branch --source=geosafe manage.py test --noinput geosafe --liveserver=0.0.0.0:8000 /usr/src/app

test: smoketest unittest

reset: down up wait sync

hardreset: pull build reset

kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Kill instance in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) kill
	@docker-compose -p $(PROJECT_ID) rm
