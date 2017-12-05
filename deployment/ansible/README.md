# Ansible Instruction README

This README provides a guideline and explanations about Ansible orchestration 
used throughout this repo. This Ansible orchestration mainly used to setup 
development environment, instead of full orchestration to maintain a production 
server. This orchestration can also be used as a baseline to create a full 
orchestration in a server. Additional work needs to be adapted to create a full 
orchestration, of course, because a full orchestration suite for production 
server is context-specific for each organizations and have different needs 
and tastes. A default baseline can be used to quickly spin up an instance 
for testing or demo purposes.

# Quick-setup working instance

To quickly setup a working instance (in local computer or on server machine). 
We included a sample `group_vars` variables that contains a simple instruction 
and highlight the default settings to modify. As a demonstrations, we will 
illustrate a different orchestration possible for different services

For all the test cases provided here, consider the following assumptions were 
set up:

- Machine capable of running docker (docker-engine installed)
- Machine capable of running ansible
- User has some basic familiarity modifying ansible variables
- User has some basic familiarity running shell commands

## Preparation

To be able to run these next instructions, you need to have this repo cloned 
somewhere in your target machine. You can run these basic git clone command:

```
git clone http://github.com/kartoza/docker-geosafe.git
```

It will create a new directory called `docker-geosafe`. This path to `docker-geosafe` 
will be called `project_path` in this instructions. You also need to initialize 
all git submodule inside (if for some reason, it is not recursively initialized).
Execute these commands from the `project_path` (from inside `docker-geosafe` dir)

```
git remote update
git submodule init
git submodule sync
git submodule update
```

These following steps are for production. To set up the development environment 
with Ansible and PyCharm Professional Edition, go to 
[the development section](#development).

## GeoNode with GeoServer backend

GeoNode in general provides default docker orchestration to easily install and 
demo it on any docker-ready machine. However, it has little documentation 
highlighting this options. Some settings also can't be made general because 
it needs some context about the local machine to make it works. To support this,
we provide an ansible vars to setup GeoNode with GeoServer backend quickly. 
You need also to modify some variables to make it work in your local machine.

1. You need to create new `all.yml` file. 

Create a new `all.yml` file and put it on `/deployment/ansible/development/group_vars/all.yml`.
Copy the content from [all.travis.geoserver.yml](development/group_vars/all.travis.geoserver.yml) as a baseline.

2. Modify your `remote_user` and `remote_group`.

Change your `remote_user` and `remote_group` to linux/mac user/group that have permissions 
to this repository and will run the GeoNode instance on the machine. For example:

```
# put your linux/mac user here
remote_user: travis
# put your linux/mac group here
remote_group: travis
```

The above sample, uses travis user and group, because it tries to run the instance 
on Travis CI.

3. Modify your `project_path`

Change your `project_path` to a directory that contains this repo in your machine.
For example:

```
# put project path
project_path: "/home/travis/build/kartoza/docker-geosafe"
```

The above sample, uses above path because that is the path in Travis CI worker 
server where this docker-geosafe repo located. Adapt this according to your 
repo location in your local machine.

4. Modify web port forward if necessary

Change the port that will host your GeoNode instance if necessary. The default
example is using default web port: 80. So user will be able to access GeoNode 
without having to specify the port.

```
docker_port_forward:
  web:
    http: 80
```

Change 80 to another port you need, if it is a different port.

5. Include your host name in ALLOWED_HOSTS django settings

Django has security features to check the name of the hosts will match the assigned hosts.
If you only use it on your local machine and will access GeoNode as http://localhost/ , 
then the default settings is already sufficient. If you need to add another hostname, include it here:

```
django:
  ALLOWED_HOSTS: "['staging.geonode.kartoza.com','localhost','django']"
```

The above sample add another hostname called http://staging.geonode.kartoza.com . 
This site is used to host our latest staging changes.

6. Modify your SITEURL django settings

SITEURL setting is needed internally by GeoNode to refer to this instance public url/address.
In staging server, for example, it was easy to setup to just fill in the hostname, 
like http://staging.geonode.kartoza.com/ or IP address in the network. 
However, in local machine installation, you need to setup a host name. This can be
done easily in Linux, we can just set the host name in `/etc/hosts` file and point to 
the correct IP address in the network. If this is not possible, you can just put 
your interface IP address in the network, so your GeoNode instance is addressable
on the network.

```
django:
  SITEURL: http://172.17.0.1/
```

The above sample uses IP address, which is the internal IP address Travis CI uses 
in their worker machine.

7. Modify your GEOSERVER_PUBLIC_LOCATION django settings

*Skip this step if you are using QGIS Server*

GEOSERVER_PUBLIC_LOCATION setting is needed internally by GeoNode to refer to its
GeoServer instance used as OGC Backend. The same rule applies with SITEURL. 
For your information, GeoServer docker container is exposed on port 8080 by default.

```
django:
  GEOSERVER_PUBLIC_LOCATION: http://172.17.0.1:8080/geoserver/
```

The above sample uses default GeoServer location which is an exposed docker container 
in port 8080. The GeoServer url is on relative url `/geoserver/` and also have the same
address as SITEURL.


8. Run your ansible setup

After modifying the necessary variables in `all.yml`, you can run Ansible orchestration
to generate all the files and docker-compose.yml file needed to spin up the instance.

Run this shortcut command here from `/deployment/` folder:
Note that, in step `make setup-ansible`, you can just press enter when asked 
about default PyCharm installation, because we didn't use it in this case.

```
make setup-ansible ANSIBLE_ARGS=--skip-tags=development
make build-geonode-core
make build
make up
# Wait a few seconds for the database to be really started.
make sync
make collectstatic
```

Explanation:

`make setup-ansible` will create all necessary files for deployment
`make build-geonode-core` will build geonode docker container as base image
`make build` will build all the services for this orchestration
`make up` will spin up all docker containers services
`make sync` will initiate first database migrations. If an error occurs during this step, have a look to the [Troubleshooting section](#troubleshooting)
`make collectstatic` will initiate first static files generation.

If you already pass through this stages, simply use `make down` to shutdown all 
containers, and `make up` again to spin up containers. Everything else is just 
needed for first time setup.

9. To view the site, go to SITEURL address

## GeoNode with QGIS Server backend

The step is similar with above [GeoNode with GeoServer backend](#geonode-with-geoserver-backend) with some differences.
This instance uses QGIS Server backend instead of GeoServer backend. 
This is the instance that we mainly develops.

1. You need to create new `all.yml` file. 

Create a new `all.yml` file and put it on `/deployment/ansible/development/group_vars/all.yml`.
Copy the content from [all.travis.qgis.yml](development/group_vars/all.travis.qgis.yml) as a baseline.

Step 2 to 6 is the same in [GeoNode with GeoServer backend](#geonode-with-geoserver-backend)

Skip step 7.

Step 8 to 9 is the same in [GeoNode with GeoServer backend](#geonode-with-geoserver-backend)

## GeoNode with QGIS Server Backend and GeoSAFE

The step is similar with above [GeoNode with QGIS Server backend](#geonode-with-qgis-server-backend) with some differences.
This instance uses QGIS Server backend instead of GeoServer backend.
This instance also includes a GeoSAFE package. A tool for using InaSAFE with GeoNode.

1. You need to create new `all.yml` file.

Create a new `all.yml` file and put it on `/deployment/ansible/development/group_vars/all.yml`.
Copy the content from [all.travis.geosafe.yml](development/group_vars/all.travis.geosafe.yml) as a baseline.

Step 2 to 5 is the same in [GeoNode with GeoServer backend](#geonode-with-geoserver-backend)

For step 6, also modify GEONODE_BASE_URL with the same value as SITEURL.

Skip step 7.

Step 8 to 9 is the same in [GeoNode with GeoServer backend](#geonode-with-geoserver-backend)

# Development

We develop using PyCharm IDE Professional Edition to streamline our debugging processs.
Unfortunetaly, PyCharm Community Edition is not supported.

PyCharm helps us quickly run different docker container services for development (geonode, 
geoserver, QGIS Server, InaSAFE headless, celery workers, rabbitmq, haproxy, 
uwsgi, nginx, etc). This also helps us to quickly debug code in celery worker 
and GeoNode, using PyCharm debugging features.

We are using Remote Debugging features. So the difference with the [Quick-setup](#quick-setup-working-instance)
is the way we treat the containers as SSH service containers. This allows us to 
attach debug process to run the service manually.

To set up development environment (with QGIS Server Backend and GeoSAFE):
 
1. You need to create new `all.yml` file.

Create a new `all.yml` file and put it on `/deployment/ansible/development/group_vars/all.yml`.
Copy the content from [all.sample.yml](development/group_vars/all.sample.yml) as a baseline.

Edit `ogc_backend` and `use_geosafe` according to your wishes about QGIS vs 
GeoServer and if you want GeoSAFE. Note if you want GeoSAFE, QGIS is compulsory.

Step 2 to 5 is the same in [GeoNode with GeoServer backend](#geonode-with-geoserver-backend)

For step 6, also modify GEONODE_BASE_URL with the same value as SITEURL.

Skip step 7 if you use QGIS

8. Run your ansible setup

Follow the step 8 from [GeoNode with QGIS Server Backend and GeoSAFE](#geonode-with-qgis-server-backend-and-geosafe), but 
instead of executing 

```
make setup-ansible ANSIBLE_ARGS=--skip-tags=development
```

execute just this instead

```
make setup-ansible
```

It will include the creation of PyCharm configuration file, so it will need 
access to modify your PyCharm settings file. Provide available PyCharm version, 
when the command asks you. After running `make setup-ansible`, you need to 
restart PyCharm completely for the new settings to take effect.

9. Run each services manually

After the new configuration takes place, it will provide you several Run Configurations.
You need to start this manually by clicking the Run Configuration button. For example,
if you setup QGIS Server with GeoSAFE, there will be 4 Run Configurations: 
Geonode Django, Geonode Celery, InaSAFE Headless, and InaSAFE Headless Analysis.

10. Using Debug Mode

You can also Run these configurations in Debug Mode by clicking the Debug Configuration
button. This will allow you to set breakpoint and halt program execution and other 
python debugging features.

11. Using Test Mode

Additionally you can run Django tests by placing your cursor at a desired test method or class,
then right-click (open context menu in mac) and choose run tests. In this manner,
the tests will run with CELERY_ALWAYS_EAGER settings, which means all celery tasks
will try to execute synchronously in the same testing thread.

# Troubleshooting


**Issue:** An exception was raised during the `make sync` about the database and migrations eg:
```
  File "/usr/local/lib/python2.7/site-packages/django/db/backends/utils.py", line 64, in execute
    return self.cursor.execute(sql, params)
django.db.utils.ProgrammingError: column base_resourcebase.alternate does not exist
LINE 1: ...loaded_preserve", "base_resourcebase"."group_id", "base_reso...
                                                             ^

Captured Task Output:
---------------------
---> pavement.sync
python manage.py makemigrations --noinput
python manage.py migrate --noinput

Build failed running pavement.sync: Subprocess return code: 1
make: *** [sync] Error 1
```

**Answer:** Migrations in GeoNode might have some issues. You should try to 
remove your previous database by removing old containers and remove the content in the `deployment/pg` folder.

For more in depth explanations, see [Detailed Troubleshooting Guide for Migration Script Mismatch](https://github.com/kartoza/docker-geosafe/wiki/Detailed-Troubleshooting-Guide-for-Migration-Script-Mismatch)
