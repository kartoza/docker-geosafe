SHELL := /bin/bash


build-db:
	@cd db && ./build.sh

build-qgis-server:
	@cd qgis-server && ./build.sh

build-nginx:
	@cd nginx && ./build.sh

build-inasafe-headless:
	@cd inasafe-headless && ./build.sh

build-django-base:
	@cd ../../../src/geonode && make build

build-django-qgis-server:
	@cd django_qgis-server && ./build.sh

build-django-geosafe:
	@cd django_geosafe && ./build.sh

build-django: build-django-qgis-server build-django-geosafe

build-all: build-db build-qgis-server build-nginx build-inasafe-headless build-django
