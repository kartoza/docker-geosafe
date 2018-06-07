#!/usr/bin/env bash

if [ -z "$REPO_NAME" ]; then
	REPO_NAME=kartoza
fi

if [ -z "$IMAGE_NAME" ]; then
	IMAGE_NAME=geonode_django_qgis-server
fi

if [ -z "$TAG_NAME" ]; then
	TAG_NAME=latest
fi

if [ -z "$BUILD_ARGS" ]; then
	BUILD_ARGS="--pull --no-cache"
fi

# Build Args Environment

if [ -z "$GEONODE_DJANGO_BASE_TAG" ]; then
	GEONODE_DJANGO_BASE_TAG=latest
fi

if [ -z "$DOCKER_GEOSAFE_TAG" ]; then
	DOCKER_GEOSAFE_TAG=develop
fi

echo "GEONODE_DJANGO_BASE_TAG=${GEONODE_DJANGO_BASE_TAG}"

echo "DOCKER_GEOSAFE_TAG=${DOCKER_GEOSAFE_TAG}"

echo "Build: $REPO_NAME/$IMAGE_NAME:$TAG_NAME"

docker build -t ${REPO_NAME}/${IMAGE_NAME} \
	--build-arg GEONODE_DJANGO_BASE_TAG=${GEONODE_DJANGO_BASE_TAG} \
	--build-arg DOCKER_GEOSAFE_TAG=${DOCKER_GEOSAFE_TAG} \
	${BUILD_ARGS} .
docker tag ${REPO_NAME}/${IMAGE_NAME}:latest ${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME}
docker push ${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME}
