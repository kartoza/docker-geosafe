# Rancher Setup Guide

This guide serves as a quick setup guide to spin GeoSAFE instances.

# Prerequisites

This guide assumes that the following requirements are met:

1. Rancher Server has been set up

If it's not, refer to [Rancher quickstart guide](http://rancher.com/docs/rancher/v1.6/en/installing-rancher/installing-server/)

2. One rancher agent has been setup to actually run the instance (it could be on the same host as the rancher server).


This guide also assumes that the user knows what Rancher is and how it works.

Take note also of the supported docker versions [here](http://rancher.com/docs/rancher/v1.6/en/hosts/#supported-docker-versions) (that link also includes quick scripts to get docker installed on your system).
 
# Creating a stack

We provid a set of `docker-compose.yml` and `rancher-compose.yml` to be used 
when creating a new stack. The related files were stored [here](../docker/compose-files). 
Simply copy paste the content of the file and put it on a relevant field when 
creating a new stack. `docker-compose.yml` content goes into the `docker-compose` field and `rancher-compose.yml`
to the `rancher-compose` field. This is the default compose file to quickly set up a new instance.
However, there are some environment variables which are dependent on how you set up 
your instance. You need to change these values depending on your environment.


## QGIS Server

A GeoNode with QGIS Server backend sample stack is stored [here](../docker/compose-files/qgis-server).

In `docker-compose.yml` file, there are some options that might need additional configuration:

1. **Volumes**

Volumes were all configured using named volumes. By default, Rancher will create
new containers with mounted volumes. These named volume will be created if the doesn't exist.
Once created, they will be persisted on the agent. So if you spin up a new service,
but mount the same named-volume, the data will be the same. You can optionally 
change these named-volume into a path location in your agent if you need to. 
Usually this is useful when you already have some data before.

2. **Django ALLOWED_HOSTS setting**

Django framework used by GeoNode will run on production mode. For security reasons,
it doesn't allow hostname that is not described in the ALLOWED_HOSTS setting. 
Simply append your hostname into this setting located in `django.environment` key
and `celery.environment` key.

3. **Django SITEURL setting**

Change this value into something your instance will be referenced from the network. 
This settinng is located in `django.environment` key and `celery.environment` key.

4. **Nginx frontend port**

The frontend that will serve the webserver is nginx by proxying uwsgi. You can specify
`nginx.ports` key into your exposed port. For example, `7000:80` will forward 
nginx 80 port into the agent 7000 port. If your agent directly serve the webserver, 
you can use `80:80` for example.

Note that all of these settings can also be changed by upgrading relevant service 
after you created the stack.

In `rancher-compose.yml` file, there are some option that might need additional configuration:

5. **Service scaling**

Scalable service in this stack are: `celery` and `qgis-server-backend`. It was scaled
to 4 by default. You can change this into other relevant value. You can also change 
this value after you created the stack.

## GeoSAFE

A GeoSAFE stack is stored [here](../docker/compose-files/geosafe). GeoSAFE stack 
is based on Geonode with QGIS Server backend. So, some options are the same, with 
additional option for GeoSAFE django app.

In `rancher-compose.yml` file:

1. Service scaling

We have additional scalable service: `inasafe-headless` and `inasafe-headless-analysis`.
