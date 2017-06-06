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
	@ansible-playbook -i ansible/development/hosts ansible/development/site.yml --syntax-check --list-tasks --list-hosts $(ANSIBLE_ARGS)

setup-ansible:
	@echo "Setup configurations using ansible"
	@ansible-playbook -i ansible/development/hosts ansible/development/site.yml $(ANSIBLE_ARGS)

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) build

sync: up
	@docker-compose -p $(PROJECT_ID) exec django django-admin.py makemigrations --noinput --merge
	@docker-compose -p $(PROJECT_ID) exec django paver sync

collectstatic: up
	@docker-compose -p $(PROJECT_ID) exec django django-admin.py collectstatic

reload:
	@docker-compose -p $(PROJECT_ID) exec django uwsgi --reload  /tmp/django.pid

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

geosafe-log:
	@docker-compose -p $(PROJECT_ID) logs -f --tail=50 django

geosafe-celery-log:
	@docker-compose -p $(PROJECT_ID) logs -f --tail=50 celery

inasafe-headless-log:
	@docker-compose -p $(PROJECT_ID) logs -f --tail=50 inasafe-headless

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
