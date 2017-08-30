FROM kartoza/geonode_django_qgis-server

# Clone source code
WORKDIR /usr/src
RUN git clone --branch 2.6.x https://github.com/kartoza/geosafe.git

WORKDIR /usr/src/app

# Upgrade dependencies
ADD geosafe-tasks-headless-celeryconfig.py /usr/src/geosafe/tasks/headless/celeryconfig.py
