FROM bitnami/python:latest 

ARG NEV
ENV TZ="Europe/Belgrade"
ENV UID=1000
ENV GID=1000
ENV DEBUG="false"
ENV WEBDAV_LOGGING_LEVEL="INFO"

COPY docker /app
COPY requirements /app/requirements
COPY app_protocols /app/

RUN \
  apt-get update \
  && mkdir /data \
  && pip install --no-cache-dir -r /app/requirements/docker.txt \
  && addgroup -S -g $GID worker \
  && adduser -S -D -G worker -u $UID -s /bin/sh worker \
  && apt-get install tzdata expat \
  && apt-get clean

WORKDIR /app
VOLUME /data
EXPOSE 8000

ENTRYPOINT /app/entrypoint.sh

LABEL org.opencontainers.image.title="AppProtocols Server"
LABEL org.opencontainers.image.author="TakiMoysha"
