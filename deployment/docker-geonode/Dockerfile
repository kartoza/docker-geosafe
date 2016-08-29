FROM geonode_django

# Toolbox
RUN apt-get -y update
RUN apt-get -y install git python-pip python-virtualenv
# Apache
RUN apt-get -y install apache2 libapache2-mod-wsgi
# QGIS-Server
RUN echo 'deb http://qgis.org/debian trusty main' >> /etc/apt/sources.list
RUN apt-get -y update
RUN apt-get -y  --allow-unauthenticated install qgis-server python-qgis libapache2-mod-fcgid
RUN export LC_ALL="C" && a2enmod fcgid && a2enconf serve-cgi-bin
RUN mkdir -p /opt/qgis-server/plugins
ADD setup-otf-plugin.sh /setup-otf-plugin.sh
RUN chmod +x /setup-otf-plugin.sh
RUN /setup-otf-plugin.sh
ADD sites-available/001-qgis-server.conf /etc/apache2/sites-available/001-qgis-server.conf
RUN a2dissite 000-default
RUN a2ensite 001-qgis-server
RUN service apache2 restart

# Upgrade dependencies
ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install --upgrade -r /REQUIREMENTS.txt
ADD setup-geonode.sh /setup-geonode.sh
RUN chmod +x /setup-geonode.sh
