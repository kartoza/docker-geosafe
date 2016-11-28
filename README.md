# Geosafe Deployment

## How to build stuffs happily

Update all submodules to retrieve all the codes

```
git submodule init
git submodule update
```

If some submodules wasn't updated correctly, add the following remote repo

```
cd src/geonode
git remote add lucernae http://github.com/lucernae/geonode.git
git fetch lucernae
cd ../

cd src/geosafe
git remote add lucernae http://github.com/lucernae/geosafe.git
git fetch lucernae
cd ../

cd src/inasafe
git remote add lucernae http://github.com/lucernae/inasafe.git
git fetch lucernae
cd ../

# Now we're in src/
git submodule update
```

Build geonode image

```
cd src/geonode
make build
make up
make down
```

We need to create new tag for newly built images of geonode/django (so it doesn't try to fetch it again from dockerhub)
This new tagged image will then be used in our entire architecture orchestration next.

```
# Find latest built images of geonode/django from previous command
docker images | grep geonode/django
# copy the image id and use it in below command
docker tag [image-id] geonode_django
```

Build all images

You can override docker-compose variable by creating docker-compose.override.yml. 
A sample file can be seen in docker-compose.override.yml.sample. Typical configuration 
is to redirect exposed ports. Or enable Pycharm Debugging.

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

  celery:
    # Loading the app is defined here to allow for
    # autoreload on changes it is mounted on top of the
    # old copy that docker added when creating the image
    volumes:
      - '../src/geonode:/usr/src/app'
    environment:
      - DEBUG=False

  nginx:
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
      - "9003:80"  # Used to expose qgis-server to localhost

  django:
    # Loading the app is defined here to allow for
    # autoreload on changes it is mounted on top of the
    # old copy that docker added when creating the image
    volumes:
      - '../src/geonode:/usr/src/app'
    environment:
      - DEBUG=True
    command: /setup-geonode.sh dev
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
    command: /setup-geonode.sh dev
    ports:
      - "9001:22"  # Used for ssh interpreter to Geonode Celery

  inasafe-headless:
    command: /start-celery.sh dev
    ports:
      - "9002:22"  # Used for ssh interpreter to InaSAFE Headless
      
  nginx:
    ports:
      - "80:80"
```

Then run the command again to update docker-compose configurations.

```
cd deployment
make build
make up
make sync
```

You can view geonode in the exposed port (default 80).


## Logging

Available logging view command

```
make geosafe-log
make geosafe-celery-log
make inasafe-headless-log
```

## PyCharm SSH Orchestration

Copy docker-compose.overrida.sample.yml as docker-compose.override.yml. This compose file will 
override some configuration to use in deployment. Some notable settings is ports and commands. 
This settings will enable ssh ready container for django, celery, and inasafe-headless.

### Creating Interpreter

Create 3 Remote Interpreter in PyCharm with corresponding services:

#### Geosafe

Use ssh port from django service. /usr/local/bin/python for interpreter path. Username root.
Password docker. Set unique name and include path mappings:

- src/geonode --> /usr/src/app
- src/core --> /usr/src/core
- src/geonode_qgis_server/geonode_qgis_server --> /usr/src/geonode_qgis_server
- src/geosafe --> /usr/src/geosafe

#### Geosafe Celery

Pretty much the same with Geosafe, but with corresponding ports for celery service.

#### InaSAFE-Headless

Use ssh port from inasafe-headless service. /usr/bin/python for interpreter path. Username root.
Password docker. Set unique name and include path mappings:

- src/inasafe --> /home/src/inasafe


### Creating Running Configuration

After creating 3 Remote Interpreter, create 3 corresponding python configuration:

#### Geosafe

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

#### Geosafe Celery

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
If the QGIS Server doesn't work (e.g. you upload a layer, and geonode doesn't the layer), one of the problem is `permission problem`. You can fix it by giving permission to write in the `qgis_layer` directory. For example:
```sudo chmod -R +066 qgis_layer/```
