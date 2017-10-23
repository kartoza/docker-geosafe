# GeoNode with QGIS Server - Rancher Setup Guide

**Contents**

* [Prerequisites](https://github.com/kartoza/docker-geosafe/blob/develop/deployment/production/docs/Rancher.md#prerequisites)
* [Creating a stack](https://github.com/kartoza/docker-geosafe/blob/develop/deployment/production/docs/Rancher.md#creating-a-stack)
* [GeoNode with QGIS Server](https://github.com/kartoza/docker-geosafe/blob/develop/deployment/production/docs/Rancher.md#geonode-with-qgis-server)
* [GeoSAFE](https://github.com/kartoza/docker-geosafe/blob/develop/deployment/production/docs/Rancher.md#geosafe)
* [Troubleshooting](https://github.com/kartoza/docker-geosafe/blob/develop/deployment/production/docs/Rancher.md#troubleshooting)


# Overview

This guide serves as a quick setup guide to spin up a GeoNode_QGIS-server or a GeoNode_QGIS-server + GeoSAFE instance. If you are new to docker and/or rancher, take a look at this video walk through so you understand the process:

[![GeoNode and Rancher Walkthrough](https://img.youtube.com/vi/lJCrbCizsmo/0.jpg)](https://www.youtube.com/watch?v=lJCrbCizsmo)

# Prerequisites

This guide assumes that the following requirements are met:

1. Docker is installed on your server. Use Ubuntu 16.04 for the best results because that is what we are testing on. For quick installation, use the [convenience scripts](http://rancher.com/docs/rancher/v1.6/en/hosts/#supported-docker-versions) provided by Rancher (make sure you choose a supported version).


2. The **stable** version of Rancher Server has been set up.

If it's not, refer to [Rancher quickstart guide](http://rancher.com/docs/rancher/v1.6/en/installing-rancher/installing-server/). Here is an example of how to run the latest stable release with a persistent mysql database stored on the file system:

```
mkdir /home/mysql
docker run -d -v /home/mysql:/var/lib/mysql --restart=unless-stopped -p 8080:8080 rancher/server:stable
```

3. One rancher agent has been set up to actually run the instance (it could be on the same host as the rancher server). Take care not to specify the ``--name`` argument when running the agent - this is not supported and will cause problems with your installation later.


# Creating the stack (automated using rancher catalogue)

An even nicer way to run the everything is to use our Rancher
Catalogue Stack for GeoServer. See [http://rancher.com](http://rancher.com) 
for more details on how to set up and configure your Rancher 
environment. Once Rancher is set up, use the Admin -> Settings menu to 
add our Rancher catalogue using this URL:

https://github.com/kartoza/kartoza-rancher-catalogue

Once your settings are saved open a Rancher environment and set up a 
stack from the catalogue's 'Kartoza' section - you will see 
GeoServer listed there.

![screen shot 2017-10-23 at 17 04 52](https://user-images.githubusercontent.com/178003/31914192-02bae616-b84a-11e7-8265-abd92bcb2dee.png)


![licecap](https://user-images.githubusercontent.com/178003/31914179-fa2a1620-b849-11e7-8b02-06cf6f99368a.gif)

(Note that there is a small mistake in the above gif - the allowed hosts entries should be quoted.

![screen shot 2017-10-23 at 17 07 15](https://user-images.githubusercontent.com/178003/31914206-13333188-b84a-11e7-8f7b-16dc8d0e60a1.png)


If you want to synchronise your GeoServer settings and database backups
(created by the nightly backup tool in the stack), use (Resilio 
sync)[https://www.resilio.com/] to create two Read/Write keys:

* one for database backups
* one for GeoServer media backups

**Note:** Resilio sync is not Free Software. It is free to use for
individuals. Business users need to pay - see their web site for details.


You can try a similar approach with Syncthing or Seafile (for free options) 
or Dropbox or Google Drive if you want to use another commercial product. These
products all have one limitation though: they require interaction 
to register applications or keys. With Resilio Sync you can completely 
automate the process without user intervention. 

# Creating a stack (manually)

We provide a set of `docker-compose.yml` and `rancher-compose.yml` files to be used 
when creating a new stack. The related files should be [here](../docker/compose-files). 
Simply copy paste the content of the file and put it on a relevant field when 
creating a new stack. `docker-compose.yml` content goes into the `docker-compose` field and `rancher-compose.yml`
to the `rancher-compose` field. This is the default compose file to quickly set up a new instance.
However, there are some environment variables which are dependent on how you set up 
your instance. You need to change these values depending on your environment. Again see the video at the top of this page if you need some background on how a stack is created in rancher.

# GeoNode with QGIS Server

A GeoNode with QGIS Server backend sample stack is stored [here](../docker/compose-files/qgis-server).

Here is the link diagram for GeoNode with QGIS Server

![screen shot 2017-09-10 at 4 52 01 pm](https://user-images.githubusercontent.com/178003/30250023-6a8082fc-9648-11e7-8d6b-e2dca9e68dfd.png)

In `docker-compose.yml` file, there are some options that might need additional configuration:

1. **Volumes**

Volumes were all configured using named volumes. By default, Rancher will create
new containers with mounted volumes. These named volume will be created if they don't exist.
Once created, they will be persisted on the agent. So if you spin up a new service,
but mount the same named-volume, the data will be the same. You can optionally 
change these named-volume into a path location in your agent if you need to. 
Usually this is useful when you have some existing data.

2. **Django ALLOWED_HOSTS setting**

The Django framework used by GeoNode will run in production mode. For security reasons,
it doesn't allow a hostname that is not described in the ALLOWED_HOSTS setting. 
Simply append your hostname into this setting located in `django.environment` key
and `celery.environment` key. Again, see the video at the top of this page for a demonstration of how you upgrade your services to set their settings.

3. **Django SITEURL setting**

Change this value into something your instance will be referenced from the network. 
This settinng is located in `django.environment` key and `celery.environment` key.

4. **Nginx frontend port**

The frontend that will serve the webserver is nginx by proxying uwsgi. You can specify
`nginx.ports` key into your exposed port. For example, `7000:80` will forward 
nginx 80 port into the agent 7000 port. If your agent directly serve the webserver, 
you can use `80:80` for example.

Note that all of these settings can also be changed by upgrading the relevant services 
after you have created the stack.

In `rancher-compose.yml` file, there are some options that might need additional configuration:

5. **Service scaling**

Scalable service in this stack are: `celery` and `qgis-server-backend`. It is scaled
to 4 by default. You can change this into other relevant value. You can also change 
this value after you have created the stack.



# GeoSAFE

GeoSAFE is GeoNode with an online version of InaSAFE bundled in. Here is the link for the diagram for GeoSAFE with QGIS Server:

![screen shot 2017-09-10 at 4 50 16 pm](https://user-images.githubusercontent.com/178003/30250019-54d67240-9648-11e7-89be-9072fbc7c896.png)

A GeoSAFE stack is stored [here](../docker/compose-files/geosafe). GeoSAFE stack 
is based on Geonode with QGIS Server backend. So, some options are the same, with 
additional option for GeoSAFE django app.

In `rancher-compose.yml` file:

1. Service scaling

We have additional scalable service: `inasafe-headless` and `inasafe-headless-analysis`.

# Troubleshooting

## Hung containers

If a service (e.g. qgis-server-backend service) is in a stale condition (stuck on rolling back but didn’t do anything), the easiest way to deal with this is to rename the service first (e.g. qgis-server-backend-old). Next clone the service into the previous name (qgis-server-backend), so we have the same service name, but with fresh containers and the same settings. Then because the qgis-server service is a load balancer to qgis-server-backend, I restart that service too. To make sure it picks up the new container instance’s internal ip.

## Gateway errors

If you try opening the web page and it says ``Gateway error``, there might be two reasons for this:

1. The django service container is dead, 
2. It doesn’t connect to nginx container (because nginx forward request to django container). 

Check the log for **django** service. If it is running it’s maybe not dead so just restart the **nginx** service to make sure it picks up the django service instance. Generally if you restart django, then you need to restart nginx, because it needs the new internal ip of django (see sequencing upgrade section below as this is the same reasone why upgrades need to happen in sequence).

## Sequencing upgrades

When upgrading / restarting services, you should take care to do things in the proper order:

1. Celery workers first
2. Django second
3. Nginx last

This will ensure that intercontainer references are maintained properly.
