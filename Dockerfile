##########################
## Build env
##########################

FROM python:3.10-buster AS BUILD

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
#RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends \
    ca-certificates pkg-config make \
    libssl-dev libffi-dev libpq-dev

# python packages
RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


##########################
## Final image
##########################
FROM python:3.10-buster

LABEL maintainer "CRG System Developers"
LABEL org.label-schema.schema-version="2.0"
LABEL org.label-schema.vcs-url="https://github.com/EGA-archive/beacon-2.x/"

# Too much ?
COPY --from=BUILD /usr/local/bin      /usr/local/bin
COPY --from=BUILD /usr/local/lib      /usr/local/lib

RUN apt-get update && \
#    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    nginx \
    && \
    rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/nginx.list && \
    apt-get purge -y --auto-remove

COPY deploy/nginx.conf        /beacon/nginx.conf
COPY deploy/supervisord.conf  /beacon/supervisord.conf
COPY deploy/entrypoint.sh     /usr/local/bin/entrypoint.sh
COPY deploy/permissions.sh     /usr/local/bin/permissions.sh
COPY beacon                   /beacon/beacon
COPY ui                       /beacon/ui

RUN groupadd beacon                              && \
    useradd -M -g beacon beacon                  && \
#    mkdir /beacon                                && \
    mkdir /var/run/beacon                        && \
    chown -R beacon:beacon /beacon               && \
#    chmod 400 /beacon/beacon/conf.py             && \
    chown -R beacon:beacon /var/log/nginx        && \
    chown -R beacon:beacon /var/lib/nginx        && \
    chown -R beacon:beacon /etc/nginx            && \
    chown -R beacon:beacon /var/run/beacon       && \
    mkdir -p /var/log/supervisord                && \
    chown -R beacon:beacon /var/log/supervisord  && \
    chmod +x /usr/local/bin/entrypoint.sh

WORKDIR /beacon
USER beacon
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
