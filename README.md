# Geosafe Deployment

## How to build stuffs happily

Update all submodules to retrieve all the codes

```
git submodule init
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
docker tag geonode/django geonode_django
```

Build all images

You can override docker-compose variable by creating docker-compose.override.yml. 
A sample file can be seen in docker-compose.override.yml.sample. Typical configuration 
is to redirect exposed ports. Or enable Pycharm Debugging

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

Create 3 Remote Interpreter in PyCharm with corresponding services:

### Geosafe

Use ssh port from django service. /usr/local/bin/python for interpreter path. Username root.
Password docker. Set unique name and include path mappings:

- src/geonode --> /usr/src/app
- src/core --> /usr/src/core
- src/geonode_qgis_server/geonode_qgis_server --> /usr/src/geonode_qgis_server
- src/geosafe --> /usr/src/geosafe

### Geosafe Celery

Pretty much the same with Geosafe, but with corresponding ports for celery service.

### InaSAFE-Headless

Use ssh port from inasafe-headless service. /usr/bin/python for interpreter path. Username root.
Password docker. Set unique name and include path mappings:

- src/inasafe --> /home/src/inasafe


After creating 3 Remote Interpreter, create 3 corresponding python configuration:

### Geosafe

Script: manage.py
Script Parameter: runserver 0.0.0.0:8000
Interpreter: Geosafe Interpreter
Environment: Copy and paste environment from the output of execution ```make geosafe-env```. You can just copy the whole environment and paste it in environment dialog in configuration modal page.

### Geosafe Celery

Script: /usr/local/bin/celery
Script Parameter: -A geosafe worker -l debug -Q default,cleanup,email,update,geosafe -n geonode.%h -B
Interpreter Gesafe Celery Interpreter
Environment: Do the same like in Geosafe Environment, but execute ```make geosafe-celery-env```

### InaSAFE-Headless

Script: /usr/local/bin/celery
Script Parameter: -A headless.celery_app worker -l info -Q inasafe-headless -n inasafe-headless.%h
Interpreter InaSAFE-Headless Interpreter
Environment: Do the same like in Geosafe Environment, but execute ```make inasafe-headless-env```


After creating this runtime configuration. You can up the services and proceed to run/debug the configuration using PyCharm commands

## Known Issue
If the QGIS Server doesn't work (e.g. you upload a layer, and geonode doesn't the layer), one of the problem is `permission problem`. You can fix it by giving permission to write in the `qgis_layer` directory. For example:
```sudo chmod -R +066 qgis_layer/```
