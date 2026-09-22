# Extend the base Python image
# See https://hub.docker.com/_/python for version options
# N.b., there are many options for Python images. We used the plain
# version number in the pilot. YMMV. See this post for a discussion of
# some options and their pros and cons:
# https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:3.6

# Give ourselves some credit
LABEL maintainer "DataMade <info@datamade.us>"

# Install any additional OS-level packages you need via apt-get. RUN statements
# add additional layers to your image, increasing its final size. Keep your
# image small by combining related commands into one RUN statement, e.g.,
#
# RUN apt-get update && \
#     apt-get install -y python-pip
#
# Read more on Dockerfile best practices at the source:
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices

# Patch to account for missing Debian Bullseye packages
RUN printf '%s\n' \
        'deb http://archive.debian.org/debian bullseye main' \
        '# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1147093' \
        'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian-security/20260831T235959Z/ bullseye-security main' \
        'deb http://archive.debian.org/debian bullseye-updates main' \
        > /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        binutils libproj-dev gdal-bin postgresql-client

# Inside the container, create an app directory and switch into it
RUN mkdir /app
WORKDIR /app

# Copy the requirements file into the app directory, and install them. Copy
# only the requirements file, so Docker can cache this build step. Otherwise,
# the requirements must be reinstalled every time you build the image after
# the app code changes. See this post for further discussion of strategies
# for building lean and efficient containers:
# https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3
COPY ./requirements.txt /app/requirements.txt
COPY ./data/requirements.txt /app/data-requirements.txt
COPY ./tests/requirements.txt /app/tests-requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -r data-requirements.txt -r tests-requirements.txt

# Copy the contents of the current host directory (i.e., our app code) into
# the container.
COPY . /app
