SHELL := /bin/bash
PROJECT_ID := geonode-docker
CONF_FILE := -f docker-compose.yml -f docker-compose.override.yml

# ----------------------------------------------------------------------------
#    P R O D U C T I O N     C O M M A N D S
# ----------------------------------------------------------------------------

up:
	# bring up the services
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) up -d

default: deploy

ansible-check:
	@echo "Check ansible command"
	@ansible -i ansible/development/hosts all -m ping
	@ansible-playbook -i ansible/development/hosts ansible/development/site.yml --syntax-check --list-tasks --list-hosts

setup-ansible:
	@echo "Setup configurations using ansible"
	@ansible-playbook -i ansible/development/hosts ansible/development/site.yml

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) build qgis-server
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) build nginx
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) build django
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) build celery
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) build inasafe-headless
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) build inasafe-headless-analysis

sync: up
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py makemigrations --noinput
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py migrate account --noinput
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py migrate --noinput
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py loaddata sample_admin
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py loaddata geonode/base/fixtures/default_oauth_apps_docker.json
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py loaddata geonode/base/fixtures/initial_data.json
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py layer_notice_types
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py migrate qgis_server --noinput --settings=core.settings
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py migrate geosafe --noinput --settings=core.settings

collectstatic: up
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django django-admin.py collectstatic

reload:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django uwsgi --reload  /tmp/django.pid

shell:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django /bin/bash

status:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) ps

dblogs:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) logs -f --tail=30 postgis

geosafe-env:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django printenv

geosafe-celery-env:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec celery printenv

inasafe-headless-env:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec inasafe-headless /bin/bash -c "source run-env-linux.sh /usr; printenv"

geosafe-log:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) logs -f --tail=50 django

geosafe-celery-log:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) logs -f --tail=50 celery

inasafe-headless-log:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) logs -f --tail=50 inasafe-headless

setup: build
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Setup in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run geonode /setup-geonode.sh
	@docker-compose -p $(PROJECT_ID) run inasafe-headless /setup-geonode.sh

wait:
	sleep 5

logs:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) logs --follow

down:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) down

pull:
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) pull

smoketest: up
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django python manage.py test geonode.tests.smoke --nocapture --detailed-errors --verbosity=1 --failfast

unittest: up
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) exec django python manage.py test geonode.people.tests geonode.base.tests geonode.layers.tests geonode.maps.tests geonode.proxy.tests geonode.security.tests geonode.social.tests geonode.catalogue.tests geonode.documents.tests geonode.api.tests geonode.groups.tests geonode.services.tests geonode.geoserver.tests geonode.upload.tests geonode.tasks.tests --noinput --failfast

test: smoketest unittest

reset: down up wait sync

hardreset: pull build reset

kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Kill instance in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) kill
	@docker-compose $(CONF_FILE) -p $(PROJECT_ID) rm
