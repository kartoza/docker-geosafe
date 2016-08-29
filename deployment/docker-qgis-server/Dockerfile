FROM ubuntu:xenial

# Toolbox
RUN apt-get -y update
RUN apt-get -y install git python-pip python-virtualenv
# Apache
RUN apt-get -y install apache2 libapache2-mod-wsgi
# QGIS-Server
RUN echo 'deb http://qgis.org/debian xenial main' >> /etc/apt/sources.list
RUN apt-get -y update
RUN apt-get -y  --allow-unauthenticated install qgis-server python-qgis libapache2-mod-fcgid
RUN export LC_ALL="C" && a2enmod fcgid && a2enconf serve-cgi-bin
ADD sites-available/001-qgis-server.conf /etc/apache2/sites-available/001-qgis-server.conf
RUN a2dissite 000-default
RUN a2ensite 001-qgis-server

# Upgrade dependencies
ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install --upgrade -r /REQUIREMENTS.txt
ADD setup-qgis-server.sh /setup-qgis-server.sh
RUN chmod +x /setup-qgis-server.sh
