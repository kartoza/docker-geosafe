FROM geonode_django

# Toolbox
RUN apt-get -y update
RUN apt-get -y install git python-pip python-virtualenv

# Upgrade dependencies
ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install --upgrade -r /REQUIREMENTS.txt
ADD setup-geonode.sh /setup-geonode.sh
ADD geosafe-tasks-headless-celeryconfig.py /celeryconfig.py
RUN chmod +x /setup-geonode.sh
