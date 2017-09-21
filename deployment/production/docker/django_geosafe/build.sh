#!/usr/bin/env bash
IMAGE_NAME=geonode_django_geosafe
TAG_NAME=latest
docker build -t kartoza/${IMAGE_NAME} .
docker tag kartoza/${IMAGE_NAME}:latest kartoza/${IMAGE_NAME}:${TAG_NAME}
docker push kartoza/${IMAGE_NAME}:${TAG_NAME}
