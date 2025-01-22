ARG QGIS_TEST_VERSION=latest
FROM  qgis/qgis:${QGIS_TEST_VERSION}
MAINTAINER Matthias Kuhn <matthias@opengis.ch>

RUN apt-get update \
    && apt-get install -y python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/

# images for QGIS<=3.34 uses much older `pip` that does not support `--break-system-packages`
RUN pip3 install -r /tmp/requirements.txt || pip3 install -r /tmp/requirements.txt --break-system-packages

ENV PYTHONPATH=/usr/share/qgis/python/plugins
ENV LANG=C.UTF-8

COPY ./ /usr/src/
RUN chmod a+x /usr/src/.docker/run-docker-tests.sh

WORKDIR /