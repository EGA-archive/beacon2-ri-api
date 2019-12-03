##########################
## Build env
##########################
FROM python:3.7-alpine3.9 AS BUILD

RUN apk add gcc postgresql-dev musl-dev libressl-dev libffi-dev make
RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

##########################
## Final image
##########################
FROM python:3.7-alpine3.9

LABEL maintainer "CRG System Developers"
LABEL org.label-schema.schema-version="2.0"
LABEL org.label-schema.vcs-url="https://github.com/EGA-archive/beacon-2.x/"

RUN apk add --no-cache --update libressl postgresql-libs

RUN addgroup beacon && \
    adduser -D -G beacon beacon && \
    mkdir /beacon

COPY --from=BUILD usr/local/lib/python3.7/ usr/local/lib/python3.7/
COPY beacon_api /beacon/beacon_api

RUN chown -R beacon:beacon /beacon
WORKDIR /beacon
USER beacon
ENTRYPOINT ["python", "-m", "beacon_api"]
