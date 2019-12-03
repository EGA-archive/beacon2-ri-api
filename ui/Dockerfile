##########################
## Build env
##########################
FROM python:3.7-alpine3.9 AS BUILD

RUN apk add gcc musl-dev libressl-dev libffi-dev make
RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /beacon
COPY beaconui /beacon/beaconui
COPY logger.yaml /beacon/logger.yaml
COPY manage.py /beacon/manage.py

# Better to reorganise manage.py (and its imported modules)
# but injecting the conf file works for now
# It's only the build stage after all. No biggy.
COPY conf.ini /beacon/conf.ini
ENV BEACON_UI_CONF=/beacon/conf.ini

WORKDIR /beacon
RUN python manage.py createcachetable

# RUN python manage.py makemigrations
# RUN python manage.py migrate

##########################
## Final image
##########################
FROM python:3.7-alpine3.9

LABEL maintainer "CRG System Developers"
LABEL org.label-schema.schema-version="2.0"
LABEL org.label-schema.vcs-url="https://github.com/EGA-archive/beacon-2.x"

RUN apk add --no-cache --update libressl

RUN addgroup beacon && \
    adduser -D -G beacon beacon && \
    mkdir /beacon

COPY beaconui /beacon/beaconui
COPY static /beacon/static
COPY templates /beacon/templates
COPY logger.yaml /beacon/logger.yaml

ENV BEACON_UI_LOG  /beacon/logger.yaml

COPY --from=BUILD usr/local/lib/python3.7/ usr/local/lib/python3.7/
COPY --from=BUILD usr/local/bin/aiohttp-wsgi-serve usr/local/bin/
COPY --from=BUILD beacon/db.sqlite beacon/db.sqlite

RUN chown -R beacon:beacon /beacon
WORKDIR /beacon
USER beacon

CMD ["aiohttp-wsgi-serve", "beaconui.wsgi:application", "--static", "/static=./static", "--host", "0.0.0.0", "--port", "8000"]


