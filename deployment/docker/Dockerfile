#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM python:3.6

LABEL maintainer="Alision Mukoma <mukomalison@gmail.com>"

RUN export DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND noninteractive
RUN dpkg-divert --local --rename --add /sbin/initctl

RUN apt-get update -y

# Install apt packages
RUN apt-get update && apt-get install -y python3-pip && \
  apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  binutils \
  python3-setuptools \
  libproj-dev \
  rpl \
  # DGDAL dependencie
  libproj-dev \
  gdal-bin

RUN echo "Installing GDAL dependencies" && \
  apt-get install -y libgeos-dev libgdal-dev && \
  # Trick is to rebuild build essential tools before gdal is reached
  apt-get install -y --reinstall build-essential \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get -y update && \
  apt-get -y auto-remove

COPY REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

# Install Node js
# RUN curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get -qqy --no-install-recommends install nodejs
# RUN bash nodesource_setup.sh
# RUN apt-get -y --force-yes install nodejs
RUN npm -g install yuglify

# Debian is messed up and aliases node as nodejs
# So when yuglify is installed it references the wrong node binary...
# lets fix that here...

RUN rpl "env node" "env nodejs" /usr/lib/node_modules/yuglify/bin/yuglify

# Install grunt
RUN npm install -g grunt-cli
ADD package.json /package.json
ADD Gruntfile.js /Gruntfile.js
RUN cd / && npm install grunt grunt-contrib-concat grunt-contrib-uglify
RUN cd / && npm install grunt-contrib-requirejs

#USER www-data
WORKDIR /home/web/django_project

ADD uwsgi.conf /uwsgi.conf

# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

CMD ["uwsgi", "--ini", "/uwsgi.conf"]
