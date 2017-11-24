# GeoSAFE (and GeoNode-QGIS_server) Deployment

This document describes the orchestration / provisioning of a GeoNode-QIS_server or a GeoNode-QIS_server + GeoSAFE service. GeoSAFE is a Django app that has a number of dependencies, including GeoNode-QIS_server. 

## Rancher orchestration

The latest (and best and easiest) way to deploy GeoNode-QIS_server by itself or with GeoSAFE is to use Rancher by following  [Rancher setup README](https://github.com/kartoza/docker-geosafe/blob/develop/deployment/production/docs/Rancher.md) 

_This readme doc needs to be refactored to put the Rancher orchestration in front and to move the Ansible and original docker-compose recipes discussed below away from the front page. They still work and may be useful in your application but we now recommend the Rancher method._

## _'One-line'_ orchestration and quick setup
  
__Ansible__ playbooks have been available since May 2017. See the bottom of this doc and in 
[Ansible setup README](deployment/ansible/README.md) for details.  

## How to build GeoSAFE with dependencies

Update all submodules to retrieve all the code

```
git remote update
git submodule init
git submodule sync
git submodule update
```

Build geonode image

```
cd deployment
make build-geonode-core
```

Now we have built a geonode docker image. This latest image will be used for 
Geonode-GeoSAFE docker images. Whenever you change your GeoNode version, you 
need to rebuild the GeoNode image.

Build all images

You can override docker-compose variables by creating docker-compose.override.yml. 
A sample file can be seen in docker-compose.override.yml.sample. Typical configuration 
is to redirect exposed ports, or enable Pycharm Debugging.

Example for production configuration:

```
version: '2'

services:

  qgis-server:
    environment:
      - DEBUG=True
      - QGIS_LOG_FILE=/tmp/qgis-server/qgis.log
      - QGIS_SERVER_LOG_FILE=/tmp/qgis-server/qgis-server.log
      # Log level 0 is the lowest (catch all), 5 is the highest (only fatal error)
      - QGIS_DEBUG=0
      - QGIS_SERVER_LOG_LEVEL=0

  django:
    # Loading the app is defined here to allow for
    # autoreload on changes it is mounted on top of the
    # old copy that docker added when creating the image
    volumes:
      - '../src/geonode:/usr/src/app'
    environment:
      - DEBUG=False
      - SITEURL=http://yourdomain/
      - GEONODE_BASE_URL=http://yourdomain/
      - QGIS_SERVER_URL=http://qgis-server/
      - GEOSERVER_BASE_URL=http://geoserver:8080/geoserver/

  celery:
    # Loading the app is defined here to allow for
    # autoreload on changes it is mounted on top of the
    # old copy that docker added when creating the image
    volumes:
      - '../src/geonode:/usr/src/app'
    environment:
      - DEBUG=False

  web:
  	# this container works by forwarding requests from nginx to uwsgi in 
  	# django container.
    ports:
      - "80:80"
```

Example for development environment to use PyCharm SSH configuration

```
version: '2'

services:

  qgis-server:
    environment:
      - DEBUG=True
      - QGIS_LOG_FILE=/tmp/qgis-server/qgis.log
      - QGIS_SERVER_LOG_FILE=/tmp/qgis-server/qgis-server.log
      # Log level 0 is the lowest (catch all), 5 is the highest (only fatal error)
      - QGIS_DEBUG=0
      - QGIS_SERVER_LOG_LEVEL=0
    ports:
      - "9003:80"  # Used to expose qgis-server to localhost for debugging

  django:
    # Loading the app is defined here to allow for
    # autoreload on changes it is mounted on top of the
    # old copy that docker added when creating the image
    volumes:
      - '../src/geonode:/usr/src/app'
    environment:
      # Make django autoreload on changes
      - DEBUG=True
    command: /usr/sbin/sshd -D
    # Start ssh service, so django can be controlled to start using
    # ssh
    ports:
      - "9000:22"  # Used for ssh interpreter to Geonode Django

  celery:
    # Loading the app is defined here to allow for
    # autoreload on changes it is mounted on top of the
    # old copy that docker added when creating the image
    volumes:
      - '../src/geonode:/usr/src/app'
    environment:
      - DEBUG=True
    command: /usr/sbin/sshd -D
    # Start ssh service, so celery can be controlled to start using
    # ssh
    ports:
      - "9001:22"  # Used for ssh interpreter to Geonode Celery

  inasafe-headless:
    command: /usr/sbin/sshd -D
    # Start ssh service, so InaSAFE worker can be controlled to start using
    # ssh
    ports:
      - "9002:22"  # Used for ssh interpreter to InaSAFE Headless
      
  inasafe-headless-analysis:
    command: /usr/sbin/sshd -D
    # Start ssh service, so InaSAFE worker can be controlled to start using
    # ssh
    ports:
      - "9004:22"  # Used for ssh interpreter to InaSAFE Headless
      
  nginx:
  # nginx works by forwarding request to django server in django container.
    ports:
      - "80:80"
```

Then run the command again to update docker-compose configurations.

```
cd deployment
make build
make up
# Wait a few seconds for the database to be really started.
make sync
```

You can view GeoNode in the exposed port (default 80).

## Development workflow

The production environment should be able to run without further modification. 
For the development environment, we are using PyCharm configuration to start all 
of these services so we can debug / monitor logs easily. This configuration 
assumes you are already familiar with PyCharm SSH debugging, Docker, Django, 
and Celery.

### In Depth Explanation

The following is an explanation of how this works in PyCharm. You can skip it 
if you're not interested.

For those who are not familiar, the concept is fairly simple. Some of the 
services that contain debuggable code (django, celery, and inasafe-headless) 
were started as ssh services with exposed ports to localhost. This allows us to 
ssh into the container and start the necessary services ourselves.

Geonode-GeoSAFE needs several services running. The core functionality of Geonode 
runs on the Django web framework. GeoSAFE is just a Django app that runs on top of GeoNode.
However, GeoSAFE also needs several services, especially InaSAFE, to run analysis.
Geonode-GeoSAFE and InaSAFE communicate using celery and message broker.
These are some examples of how to run each service manually.

To run a Django container in debug mode, we need to run the Django server in it.

```
# ssh into django container (exposed port is 9000 in docker-compose.override.yml)
ssh root@localhost -p 9000
# password: docker
cd /usr/src/app
# Run django server on 8000 port, so it will be forwarded to localhost via nginx.
python manage.py runserver 0.0.0.0:8000
```

This way, as long as it is running, it will provide logs. You can continue 
with your Django development workflow as usual. This is just to show how to 
run Django server from inside the container. If you're familiar with Docker, 
it is fairly straightforward to understand.

Next, we need to run celery workers. It is recommendeded if 
you understand celery concepts. We need three workers for GeoSAFE. 
The first celery worker handles Geonode tasks. 

```
# ssh into geonode celery container (exposed port is 9001 in the 
# docker-compose.override.yml example)
ssh root@localhost -p 9001
# password: docker
cd /usr/src/app
# Run celery worker (broker settings were already configured)
# This command runs several queue (default,cleanup,email,update,geosafe) 
# with debug log level, and activates celerybeat.
celery -A geosafe worker -l debug -Q default,cleanup,email,update,geosafe -n geonode.%h -B
```

The second one starts up a celery worker for InaSAFE that handles layer and 
metadata queries

```
# ssh into InaSAFE-Headless celery container (exposed port is 9002 in the
# docker-compose.override.yml example)
ssh root@localhost -p 9002
# password: docker
cd /home/src/inasafe
# We already provide a short script to run the service:
/start-celery.sh prod inasafe-headless
# If you look at the file, it is basically calls the following worker commands:
celery -A headless.celery_app worker -l info -Q inasafe-headless -n inasafe-headless.%h
```

The third one starts up a celery worker for InaSAFE that handles analysis

```
# ssh into InaSAFE-Headless celery container (exposed port is 9004 in the
# docker-compose.override.yml example)
ssh root@localhost -p 9004
# password: docker
cd /home/src/inasafe
# We already provide a short script to run the service:
/start-celery.sh prod inasafe-headless-analysis
# If you look at the file, it is basically calls the following worker commands:
celery -A headless.celery_app worker -l info -Q inasafe-headless-analysis -n inasafe-headless-analysis.%h
```

These conclude the necessary tasks to run services needed by GeoSAFE. Also note 
that Django web server supports hot-loading, meaning that if you changed some 
code in GeoNode or GeoSAFE, it will be interpreted immediately by the Django web 
server. Meanwhile, if you changed celery tasks code, you need to rerun the 
relevant worker for the changes to be applied. Celery workers don't support 
hot-loading.

## Logging

Available logging view command

```
make geosafe-log
make geosafe-celery-log
make inasafe-headless-log
```

## PyCharm SSH Orchestration

We used PyCharm for our development environment. In the professional edition, 
we are able to use SSH interpreter to debug code, and use Run Configuration 
to orchestrate the services.

### Ansible generated files

We are using ansible to setup pycharm configurations. To use this, in the directory
deployment/ansible/development/group_vars/ copy/paste all.sample.yml to all.yml.
Use that file as template and modify it according to your environment.
For example, these are common changes needed:

```
# Use either qgis_server or geoserver
ogc_backend: qgis_server
# set to True or False to include geosafe in the orchestration
use_geosafe: True
remote_user: your username
remote_group: your username group
project_path: the location of this repository in your computer path
docker_port_forward: you might want to change several port redirection
django: you might want to change SITEURL and GEONODE_BASE_URL to your local ip 
		interface
```

After setting this up, run

```
make setup-ansible
```

and follow further instructions in the command line.

You need to relaunch the ansible playbook everytime your IP is updated.
Otherwise, Geonode will try to fetch some resources with an IP out of date.

### Creating Interpreter without using ansible

Copy docker-compose.overrida.sample.yml as docker-compose.override.yml. This compose file will 
override some configurations to use in deployment. Some notable settings are ports and commands. 
These settings will enable ssh ready containers for django, celery, and inasafe-headless.

Create 3 Remote Interpreters in PyCharm with corresponding services:

#### GeoSAFE

Use ssh port from django service. /usr/local/bin/python for interpreter path. Username root.
Password docker. Set unique name and include path mappings:

- src/geonode --> /usr/src/app
- src/core --> /usr/src/core
- src/geonode_qgis_server/geonode_qgis_server --> /usr/src/geonode_qgis_server
- src/geosafe --> /usr/src/geosafe

#### GeoSAFE Celery

Pretty much the same as with GeoSAFE, but with corresponding ports for celery service.

#### InaSAFE-Headless

Use ssh port from inasafe-headless service. /usr/bin/python for interpreter path. Username root.
Password docker. Set unique name and include path mappings:

- src/inasafe --> /home/src/inasafe

### Creating Running Configuration

After creating 3 Remote Interpreter, create 3 corresponding python configuration:

#### GeoSAFE

Script: manage.py

Script Parameter: runserver 0.0.0.0:8000

Interpreter: Geosafe Interpreter

Environment: Copy and paste environment from the output of execution ```make geosafe-env```. You can just copy the whole environment and paste it in environment dialog in configuration modal page.

Sample of Environment configurations. Modified accordingly:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PYTHONPATH=/usr/src:/usr/src/app/
NOTVISIBLE=in users profile
ROOT_URLCONF=core.urls
DB_USER=postgres
DB_NAME=postgres
DEBUG=True
LANG=C.UTF-8
BROKER_URL=amqp://guest:guest@rabbitmq:5672/
PYTHON_PIP_VERSION=6.1.1
DJANGO_SETTINGS_MODULE=core.settings
PYTHONUNBUFFERED=1
DATABASE_URL=postgres://docker:docker@postgis:5432/gis
GEOSERVER_BASE_URL="http://geoserver:8080/geoserver/"
DB_PASS=postgres
ALLOWED_HOSTS=['django',]
GEONODE_BASE_URL=http://nginx/
QGIS_SERVER_URL=http://qgis-server/
PYTHON_VERSION=2.7.9
SITEURL=http://localhost/
```

#### GeoSAFE Celery

Script: /usr/local/bin/celery

Script Parameter: -A geosafe worker -l debug -Q default,cleanup,email,update,geosafe -n geonode.%h -B

Interpreter Gesafe Celery Interpreter

Environment: Do the same like in Geosafe Environment, but execute ```make geosafe-celery-env```

Sample of Environment configurations. Modified accordingly:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PYTHONPATH=/usr/src:/usr/src/app/
NOTVISIBLE=in users profile
ROOT_URLCONF=core.urls
C_FORCE_ROOT=1
DB_USER=postgres
DB_NAME=postgres
DEBUG=True
LANG=C.UTF-8
BROKER_URL=amqp://guest:guest@rabbitmq:5672/
PYTHON_PIP_VERSION=6.1.1
DJANGO_SETTINGS_MODULE=core.settings
DATABASE_URL=postgres://docker:docker@postgis:5432/gis
GEOSERVER_BASE_URL="http://geoserver:8080/geoserver/"
DB_PASS=postgres
ALLOWED_HOSTS=['django',]
GEONODE_BASE_URL=http://nginx/
QGIS_SERVER_URL=http://qgis-server/
PYTHON_VERSION=2.7.9
SITEURL=http://localhost/
```

#### InaSAFE-Headless

Script: /usr/local/bin/celery

Script Parameter: -A headless.celery_app worker -l info -Q inasafe-headless -n inasafe-headless.%h

Interpreter InaSAFE-Headless Interpreter

Environment: Do the same like in Geosafe Environment, but execute ```make inasafe-headless-env```

Sample of Environment configurations. Modified accordingly:

```
PATH=/usr/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
INASAFE_LOCALE=id
NOTVISIBLE=in users profile
C_FORCE_ROOT=True
QGIS_PATH=/usr
INASAFE_HEADLESS_DEPLOY_OUTPUT_URL=http://inasafe-output/output/
INASAFE_POPULATION_PATH=/home/src/inasafe/realtime/fixtures/exposure/population.tif
INASAFE_HEADLESS_BROKER_HOST=amqp://guest:guest@rabbitmq:5672/
DISPLAY=:99
INASAFE_REALTIME_REST_USER=test@realtime.inasafe.org
LD_LIBRARY_PATH=/usr/lib
QGIS_LOG_FILE=/tmp/inasafe/realtime/logs/qgis.log
INASAFE_REALTIME_REST_URL=http://localhost:8000/realtime/api/v1/
QGIS_DEBUG_FILE=/tmp/inasafe/realtime/logs/qgis-debug.log
PYTHONPATH=/usr/share/qgis/python:/usr/share/qgis/python/plugins:/home/src/inasafe
INASAFE_HEADLESS_DEPLOY_OUTPUT_DIR=/home/output/
QGIS_PREFIX_PATH=/usr
INASAFE_WORK_DIR=/tmp/inasafe
INASAFE_SENTRY=1
INASAFE_REALTIME_REST_LOGIN_URL=http://localhost:8000/realtime/api-auth/login/
PYTHONUNBUFFERED=1
DEBIAN_FRONTEND=noninteractive
INASAFE_REALTIME_REST_PASSWORD=t3st4ccount
QGIS_DEBUG=0
```

#### InaSAFE-Headless Analysis

Same with InaSAFE-Headless, but change this:

Script Parameter: -A headless.celery_app worker -l info -Q inasafe-headless-analysis -n inasafe-headless-analysis.%h

After creating this runtime configuration. You can up the services and proceed to run/debug the configuration using PyCharm commands

## Known Issue
If the QGIS Server doesn't work (e.g. you upload a layer, and GeoNode doesn't publish the layer), one of the problems could be `permission problem`. You can fix it by setting write permission in the `qgis_layer` directory. For example:
```sudo chmod -R +066 qgis_layer/```

## Deploying Staging

Deploying to staging server has made easier thanks to Ansible. 

Before following the below steps, make sure that you have permissions from an admin-level user to access `docker-geosafe-staging` repo.

These steps assume that you have got access from a user named *lucernae* in the gitlab. 

Therefore, the repo would be: https://gitlab.com/lucernae/docker-geosafe-staging

* Clone *docker-geosafe-staging* to your local machine

  Run `git clone https://gitlab.com/lucernae/docker-geosafe-staging`

  Assume your parent directory is `/home/data`. Then, you now have `/home/data/docker-geosafe-staging` with a subfolder named **ansible**, and two files: **Makefile** and **README.md**.

* When you have obtained permission to deploy staging, your public key is added to the `docker-geosafe-staging` and the staging server by the admin. 

  Now, you need to make sure that the server information is in your local `~/.ssh/config`. 
  
  Type: `more ~/.ssh/config` and make sure that the server information matches the one from `/home/data/docker-geosafe-staging/ansible/ssh-config/config`. If not, copy the server information from `/home/data/docker-geosafe-staging/ansible/ssh-config/config` to `~/.ssh/config`.
  
* Check if you can connect to the server using ssh by typing: `ssh <user>@<staging-ip-address>`. 

* If the connection succeed, exit `ssh`, go to `/home/data/docker-geosafe-staging` and type: `make play-staging`. 

* The deploying process is now ready to go. 

* But, wait.... there are a few questions before deploying really takes place:

  * Force checkout to latest update
  
    Default: **No**
    
    Leaves to the default **No** if you have played around on the staging server and don't want the changes to be purged. 
    
  * Update to snapshot in docker-geosafe?
  
    Default: ** Yes**
    
    Obtains the latest changes from `http://github.com/kartoza/docker-geosafe`. Current branch is *develop*.
    
  * Update to latest submodules?
  
    Default: **Yes**
    
    Obtains the latest changes from *geonode, geosafe, inasafe, otf-project* submodules.
    
  * Import default data?
  
    Default: **No**
    
    Just press enter if you would like to keep the current data on the staging intact.
    
Once you answer all the questions, the deploying process begins. 

You should see messages like:

```
PLAY [Setup staging auto deploy] ***********************************************

TASK [setup] *******************************************************************
Enter passphrase for key '/Users/<your-name>/.ssh/id_rsa': 
ok: [staging.geonode.kartoza.com]

TASK [requirements : ensure apt packages installed] ****************************
changed: [staging.geonode.kartoza.com] => (item=[u'nginx', u'libssl-dev'])

TASK [requirements : ensure packages installed] ********************************
ok: [staging.geonode.kartoza.com] => (item=pexpect)
changed: [staging.geonode.kartoza.com] => (item=docker-compose)
changed: [staging.geonode.kartoza.com] => (item=ansible)

TASK [requirements : copy nginx sites available] *******************************
ok: [staging.geonode.kartoza.com]

TASK [requirements : link to nginx sites enabled] ******************************
ok: [staging.geonode.kartoza.com]
TASK [requirements : restart nginx] ********************************************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch latest changes of docker-geosafe] ********************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch Remote update] ***************************************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch Remote update geonode] *******************************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch Remote update geosafe] *******************************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch Remote update inasafe] *******************************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch Remote update otf-project] ***************************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch latest changes of geonode] ***************************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch latest changes of geosafe] ***************************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch latest changes of inasafe] ***************************
changed: [staging.geonode.kartoza.com]

TASK [update_repo : Fetch latest changes of otf-project] ***********************
changed: [staging.geonode.kartoza.com]

TASK [docker_compose : customize docker-compose.yml] ***************************
changed: [staging.geonode.kartoza.com]

TASK [inasafe_headless : customize InaSAFE celeryconfig] ***********************
ok: [staging.geonode.kartoza.com]

TASK [geonode : create qgis layer directory] ***********************************
changed: [staging.geonode.kartoza.com] => (item=qgis_layer)
changed: [staging.geonode.kartoza.com] => (item=qgis_tiles)

TASK [geosafe : customize geosafe celeryconfig] ********************************
ok: [staging.geonode.kartoza.com]

TASK [orchestrate : shutdown container] ****************************************
changed: [staging.geonode.kartoza.com]

TASK [orchestrate : build container] *******************************************
changed: [staging.geonode.kartoza.com]

TASK [orchestrate : startup container] *****************************************
changed: [staging.geonode.kartoza.com]

TASK [orchestrate : wait postgis to startup] ***********************************
Pausing for 20 seconds
(ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)
ok: [staging.geonode.kartoza.com]

TASK [orchestrate : run collectstatic] *****************************************
changed: [staging.geonode.kartoza.com]

TASK [orchestrate : reload uwsgi] **********************************************
changed: [staging.geonode.kartoza.com]
... etc ...
```

