export COMPOSE_PROJECT_NAME=geonode-docker
export COMPOSE_FILE=docker-compose.yml:docker-compose.override.yml
SHELL := /bin/bash
DELAY = 5

# ----------------------------------------------------------------------------
#    P R O D U C T I O N     C O M M A N D S
# ----------------------------------------------------------------------------

up:
	# bring up the services
	@docker-compose up -d --remove-orphans ${ARGS}

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
	@cd ../src/geonode; docker pull kartoza/geonode:2.8.0; docker-compose build --build-arg GEONODE_BASE_IMAGE=kartoza/geonode:2.8.0 django; docker tag geonode/geonode:latest kartoza/geonode_django_base:latest

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose build

default-scale:
	@docker-compose scale qgis-server=1 qgis-server-backend=1 celery=1 inasafe-headless=1 inasafe-headless-analysis=1

production-scale:
	@docker-compose scale qgis-server=1 qgis-server-backend=4 celery=4 inasafe-headless=4 inasafe-headless-analysis=4

sync: up
	@docker-compose exec django django-admin.py makemigrations --noinput --merge
	@docker-compose exec django paver sync

collectstatic: up
	@docker-compose exec django django-admin.py collectstatic

static-development-setup:
	@echo "Nodejs and NPM are prerequisites"
	@echo "Make sure these are installed before running this command."
	@cd ../src/geonode/geonode/static; npm install --save-dev; bower install

static-grunt-production:
	@echo "Make sure static development command were setup before running this command."
	@cd ../src/geonode/geonode/static; grunt production

geosafe-unittests-worker:
	@docker-compose run --rm -d -e CELERY_TESTING_WORKER=True --entrypoint="" celery /usr/local/bin/celery -A geosafe worker -l debug -Q default,cleanup,email,update,geosafe -n geonode.%h -B

geosafe-coverage-unittests-worker:
	@docker-compose run --rm -d --entrypoint="" -e CELERY_TESTING_WORKER=True -e COVERAGE_PROCESS_START=/usr/src/geosafe/.coveragerc celery coverage run --rcfile=/usr/src/geosafe/.coveragerc /usr/local/bin/celery -A geosafe worker -l debug -P solo -Q default,cleanup,email,update,geosafe -n geonode.%h -B

geosafe-coverage-unittests-worker-kill:
	@docker kill --signal=SIGINT geonode-docker_celery_run_1
	@sleep 5
	@docker rm geonode-docker_celery_run_1

reload:
	@docker-compose exec django uwsgi --reload  /tmp/django.pid

restart-qgis-server:
	@docker-compose restart qgis-server-backend

restart-celery:
	@docker-compose restart celery
	@docker-compose restart inasafe-headless
	@docker-compose restart inasafe-headless-analysis

shell:
	@docker-compose exec django /bin/bash

db-shell:
	@docker-compose exec db /bin/bash

postgis-shell:
	@docker-compose exec db su - postgres -c "psql"

status:
	@docker-compose ps

db-logs:
	@docker-compose logs -f --tail=30 db

geosafe-env:
	@docker-compose exec django printenv

geosafe-celery-env:
	@docker-compose exec celery printenv

inasafe-headless-env:
	@docker-compose exec inasafe-headless /bin/bash -c "source run-env-linux.sh /usr; printenv"

qgis-server-backend-log:
	@docker-compose logs -f --tail=50 qgis-server-backend

geosafe-log:
	@docker-compose logs -f --tail=50 django

geosafe-celery-log:
	@docker-compose logs -f --tail=50 celery

inasafe-headless-log:
	@docker-compose logs -f --tail=50 inasafe-headless

inasafe-headless-analysis-log:
	@docker-compose logs -f --tail=50 inasafe-headless-analysis

setup: build
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Setup in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose run geonode /setup-geonode.sh
	@docker-compose run inasafe-headless /setup-geonode.sh

wait:
	sleep $(DELAY)

logs:
	@docker-compose logs --follow django

remove-test-db:
	@docker-compose stop db
	@docker-compose run --rm --entrypoint="" db /bin/bash -c "service postgresql start; su - postgres -c \"sleep 5;psql -l;dropdb unittests;psql -l\"; service postgresql stop"
	@docker-compose up -d db

down:
	@docker-compose down --remove-orphans ${ARGS}

pull:
	@docker-compose pull

smoketest: up
	@docker-compose exec django python manage.py test geonode.tests.smoke --nocapture --detailed-errors --verbosity=1 --failfast

unittest: up
	@docker-compose exec django python manage.py test geonode.people.tests geonode.base.tests geonode.layers.tests geonode.maps.tests geonode.proxy.tests geonode.security.tests geonode.social.tests geonode.catalogue.tests geonode.documents.tests geonode.api.tests geonode.groups.tests geonode.services.tests geonode.geoserver.tests geonode.upload.tests geonode.tasks.tests --noinput --failfast

geosafe-coverage-test:
	@docker-compose exec django /bin/bash -c "export TESTING=True; export COVERAGE_PROCESS_START=/usr/src/geosafe/.coveragerc; coverage run --rcfile=/usr/src/geosafe/.coveragerc manage.py test geosafe --noinput --liveserver=0.0.0.0:8000 --nomigrations"

test: smoketest unittest

reset: down up wait sync

hardreset: pull build reset

kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Kill instance in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose kill
	@docker-compose rm
