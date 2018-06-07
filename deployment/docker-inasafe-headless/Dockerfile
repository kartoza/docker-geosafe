#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM kartoza/qgis-desktop:2.18

RUN apt-get -y update; apt-get -y --force-yes install pwgen git inotify-tools

# This section taken on 2 July 2015 from
# https://docs.docker.com/examples/running_ssh_service/
# Sudo is needed by pycharm when it tries to pip install packages
RUN apt-get update -y; apt-get install -y --force-yes openssh-server sudo
RUN mkdir /var/run/sshd
RUN echo 'root:docker' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# End of cut & paste section

#-------------Application Specific Stuff ----------------------------------------------------
# Install git, xvfb
RUN apt-get -y update; apt-get -y --force-yes install git xvfb python-setuptools python-dev libssl-dev libffi-dev
RUN easy_install pip==9.0.1
ADD REQUIREMENTS.txt /REQUIREMENTS.txt
ADD REQUIREMENTS-headless.txt /REQUIREMENTS-headless.txt
ADD REQUIREMENTS-realtime.txt /REQUIREMENTS-realtime.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS-headless.txt
RUN pip install -r /REQUIREMENTS-realtime.txt
# Copy ubuntu fonts
RUN apt-get -y --force-yes install wget unzip
ADD ubuntu-font-family-0.83.zip /ubuntu-font-family-0.83.zip
RUN unzip ubuntu-font-family-0.83.zip
RUN mv ubuntu-font-family-0.83 /usr/share/fonts/truetype/ubuntu-font-family
CMD fc-cache -f -v

ADD start-celery.sh /start-celery.sh
ADD headless-celeryconfig.py /celeryconfig.py
RUN chmod +x /start-celery.sh
