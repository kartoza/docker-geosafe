# Docker Image Build Procedure

This document serves as a guide to build docker image manually
Because some of the images are dependent on the code, whenever the code
changes, we need to manually build the image. Although these images
were built automatically using docker cloud triggers, there are some cases
that we have to manually built the images because of the interdependencies
can not be resolved easily by docker cloud.

## How to perform the instruction

The instruction will be provided as a shorthand. You need to

### Build Context

To build the image, you need to `cd` into the path where `Dockerfile` exists
for that particular image. If you see a declaration like this:

```
build_context: qgis-server
```

That means you need to go into this directory (click to follow the location) [qgis-server](../docker/qgis-server)

### ARG Options

Some image will have zero, one or more ARG options. There is a default value
for this ARG options, but if you can specify a custom value. If you see a declaration
like this:

```
arg:
	OTF_PROJECT_TAG: master
```

That means you can specify a custom value, **before** you build
the image. To specify a custom arg value, use `export` in your terminal.

```
export OTF_PROJECT_TAG=new_latest_cool_develop_tag
```

If you didn't use export, it will use a default value, which can be seen in
the associated `Dockerfile`.

### Image Building

Simply go to where the build context is located and execute this:

```
docker build -t ${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME} .
```

Where `REPO_NAME`, `IMAGE_NAME`, and `TAG_NAME` will be provided in the instruction.
You can replace it yourself in the command, or do export first.
For example, you can do this:

Provided that:

```
REPO_NAME: kartoza
IMAGE_NAME: geonode_qgis-server
TAG_NAME: latest
```

You can do either this:

```
docker build -t kartoza/geonode_qgis-server:latest .
```

or this:

```
export REPO_NAME=kartoza
export IMAGE_NAME=geonode_qgis-server
export TAG_NAME=latest
docker build -t ${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME} .
```

### Image Pushing

Simply execute this command **after** you build the particular image

```
docker push ${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME}
```

Make sure you already login to docker cloud using this command:

```
docker login
```

Pushing an image have an implicit requirements that you have the access to that repo

# Independent Images

For this type of image, it tends to be relatively stable. So, we don't have to
build it often.

## QGIS Server

Simply build the image.

```
build_context: /deployment/production/docker/qgis-server
arg:
	OTF_PROJECT_TAG=master
REPO_NAME: kartoza
IMAGE_NAME: geonode_qgis-server
TAG_NAME: latest
```

## Nginx

Simply build the image.

```
build_context: /deployment/production/docker/nginx
REPO_NAME: kartoza
IMAGE_NAME: geonode_nginx
TAG_NAME: latest
```

## Db (Postgis)

Simply build the image.

```
build_context: /deployment/production/docker/db
REPO_NAME: kartoza
IMAGE_NAME: geonode_db
TAG_NAME: latest
```

## InaSAFE Headless

Simply build the image.

```
build_context: /deployment/production/docker/inasafe-headless
arg:
	INASAFE_HEADLESS_TAG: realtime-backport-cherry-pick
REPO_NAME: kartoza
IMAGE_NAME: geonode_inasafe-headless
TAG_NAME: latest
```

# Interdependent Image

For these particular images, the order of which they created is important.
Because some images will be used as a base for others.

## GeoNode Django Base

You need to manually do fresh pull from geonode/django. Because it contains
build trigger. Do this command before building the image.

```
docker pull geonode/django:latest
```

Then proceed to build the image. Make sure to clear out any unimportant files
inside the build context, because it will be copied to the image!

```
build_context: /src/geonode
```

Or do a fresh clone to a tagged branch of your choice.
For example, this will checkout `master-qgis_server` branch.


```
cd /tmp
git clone --branch master-qgis_server --depth 1 https://github.com/kartoza/geonode.git
cd geonode
```

Then, proceed to build the image.

```
REPO_NAME: kartoza
IMAGE_NAME: geonode_django_base
TAG_NAME: latest
```

## GeoNode + QGIS Server django app

You need to have base image: kartoza/geonode_django_base already built in your
local machine (or pull from cloud if you already push)

```
build_context: /deployment/production/docker/django_qgis-server
arg:
	GEONODE_DJANGO_BASE_TAG: latest
	DOCKER_GEOSAFE_TAG: develop
REPO_NAME: kartoza
IMAGE_NAME: geonode_django_qgis-server
TAG_NAME: latest
```

## GeoNode + QGIS Server django app + GeoSAFE django app

You need to have base image: kartoza/geonode_django_qgis-server already built in your
local machine (or pull from cloud if you already push)

```
build_context: /deployment/production/docker/django_geosafe
arg:
	GEONODE_DJANGO_QGIS_SERVER_TAG: latest
	GEOSAFE_TAG: 2.6.x
REPO_NAME: kartoza
IMAGE_NAME: geonode_django_geosafe
TAG_NAME: latest
```

# Customizing your profile

Once you understand how the build works, you can customize your build profile.
For example, you might want to tag the image as a different one, or use different
Libary combination.
