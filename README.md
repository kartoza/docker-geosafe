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
```

Build all images

You can override docker-compose variable by creating docker-compose.override.yml. 
A sample file can be seen in docker-compose.override.yml.sample. Typical configuration 
is to redirect exposed ports.

```
cd deployment
make build
make up
make sync
```

You can view geonode in the exposed port (default 80).
