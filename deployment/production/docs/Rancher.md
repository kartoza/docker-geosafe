# Rancher Setup Guide

This guide serves as a quick setup guide to spin GeoSAFE instances.

# Prerequisites

This guide assumes that the following requirements are met:

1. Rancher Server were setup

If it's not, refer to [Rancher quickstart guide](http://rancher.com/docs/rancher/v1.6/en/installing-rancher/installing-server/)

2. One rancher agent were setup to actually run the instance


This guide also assumes that the user knows what Rancher is and how does it work.
 
# Creating a stack

We provided a set of `docker-compose.yml` and `rancher-compose.yml` to be used 
when creating a new stack. The related files were stored [here](../docker/compose-files). 
Simply copy paste the content of the file and put it on a relevant field when 
creating a new stack. `docker-compose.yml` to `docker-compose` field and `rancher-compose.yml`
to `rancher-compose`. This is the default compose file to quickly setup a new instance.
However, there are some environment variables which is dependent on how you setup 
your instance. You need to change the value depending on your environment.


## QGIS Server

A Geonode with QGIS Server backend sample stack is stored [here](../docker/compose-files/qgis-server).

In `docker-compose.yml` file, there are some options that might need additional configuration:

1. Volumes

Volumes were all configured using named volume. By default, Rancher will create
new container with mounted volumes. These named volume will be created if it doesn't exists.
Once created, it will be persisted on the agent. So if you spin up a new service,
but mounting the same named-volume, the data will be the same. You can optionally 
change these named-volume into a path location in your agent if you need to. 
Usually this is useful when you already have some data before.

2. Django ALLOWED_HOSTS setting

Django framework used by Geonode will run on production mode. For security reasons,
it doesn't allow hostname that is not described in the ALLOWED_HOSTS setting. 
Simply append your hostname into this setting located in `django.environment` key
and `celery.environment` key.

3. Django SITEURL setting

Change this value into something your instance will be referenced from the network. 
This settinng is located in `django.environment` key and `celery.environment` key.

4. Nginx frontend port

The frontend that will serve the webserver is nginx by proxying uwsgi. You can specify
`nginx.ports` key into your exposed port. For example, `7000:80` will forward 
nginx 80 port into the agent 7000 port. If your agent directly serve the webserver, 
you can use `80:80` for example.

Note that all of these settings can also be changed by upgrading relevant service 
after you created the stack.

In `rancher-compose.yml` file, there are some option that might need additional configuration:

1. Service scaling

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
