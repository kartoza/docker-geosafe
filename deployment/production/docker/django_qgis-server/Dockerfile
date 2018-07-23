ARG GEONODE_DJANGO_BASE_TAG=latest
FROM kartoza/geonode_django_base:${GEONODE_DJANGO_BASE_TAG}

ADD uwsgi.conf /uwsgi.conf

# Clone source code
WORKDIR /tmp
ARG DOCKER_GEOSAFE_TAG=develop
RUN git clone --branch ${DOCKER_GEOSAFE_TAG} --depth 1 https://github.com/kartoza/docker-geosafe.git
RUN mv /tmp/docker-geosafe/src/core /usr/src/core

WORKDIR /usr/src/app

# Upgrade dependencies
ADD entry-point.sh /entry-point.sh
ADD uwsgi.conf /uwsgi.conf
ADD wait-for-databases /usr/bin/wait-for-databases
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN chmod +x /entry-point.sh

ENTRYPOINT ["/entry-point.sh"]
CMD ["prod"]
