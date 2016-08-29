#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
#FROM inasafe/qgis-desktop:2.4
#MAINTAINER Akbar Gumbira <akbargumbira@gmail.com>
#FROM kartoza/qgis-desktop:2.8.4
FROM debian:jessie

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 3FF5FFCAD71472C4

RUN echo "deb     http://qgis.org/debian jessie main" >> /etc/apt/sources.list
RUN echo "deb-src http://qgis.org/debian jessie main" >> /etc/apt/sources.list
#RUN echo "deb http://ppa.launchpad.net/ubuntugis/ubuntugis-unstable/ubuntu trusty main" >> /etc/apt/sources.list
#RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ trusty universe" >> /etc/apt/sources.list

RUN apt-get -y update; apt-get -y install qgis python-qgis
RUN apt-get -y --force-yes install build-essential autoconf libtool pkg-config
#RUN pip install cython

RUN export DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND noninteractive
RUN dpkg-divert --local --rename --add /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not wish to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN apt-get -y update
RUN apt-get -y --force-yes install pwgen git inotify-tools

#-------------Application Specific Stuff ----------------------------------------------------
# Install git, xvfb
RUN apt-get -y install git xvfb python-setuptools python-dev libssl-dev libffi-dev
RUN easy_install pip==7.1.2
ADD REQUIREMENTS.txt /REQUIREMENTS.txt
ADD REQUIREMENTS-headless.txt /REQUIREMENTS-headless.txt
ADD REQUIREMENTS-realtime.txt /REQUIREMENTS-realtime.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS-headless.txt
RUN pip install -r /REQUIREMENTS-realtime.txt
# Copy ubuntu fonts
RUN apt-get -y install wget unzip
RUN wget -c http://font.ubuntu.com/download/ubuntu-font-family-0.83.zip
RUN unzip ubuntu-font-family-0.83.zip
RUN mv ubuntu-font-family-0.83 /usr/share/fonts/truetype/ubuntu-font-family
CMD fc-cache -f -v

ADD start-celery.sh /start-celery.sh
RUN chmod +x /start-celery.sh
