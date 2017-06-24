# Orchestration Changelog

This will keep track what the current orchestration able to do.


1. Add GeoSAFE options

Add the following Makefile commands:

```
make inasafe-headless-analysis-log
make restart-celery
```

Add the following GeoSAFE options to all.sample.yml:

```
django:
  # GeoSAFE specific settings
  USE_LAYER_FILE_ACCESS: True
  INASAFE_LAYER_DIRECTORY: "/home/geosafe/media/"
  INASAFE_LAYER_DIRECTORY_BASE_PATH: "/usr/src/app/geonode/uploaded/"
  GEOSAFE_IMPACT_OUTPUT_DIRECTORY: "/home/geosafe/impact_layers"
  INASAFE_IMPACT_BASE_URL: "/output/"
  USE_LAYER_HTTP_ACCESS: False
```
