##########################
## Build env
##########################
FROM python:buster AS BUILD

ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends \
    ca-certificates pkg-config patch git gcc g++ make \
    bzip2 libssl-dev libffi-dev libpq-dev \
    ; \
    rm -rf /var/lib/apt/lists/*; \
    pip install --upgrade pip; \
    pip install -r /tmp/requirements.txt

##########################
## Final image
##########################
FROM python:buster

LABEL maintainer "CRG System Developers"
LABEL org.label-schema.schema-version="2.0"
LABEL org.label-schema.vcs-url="https://github.com/EGA-archive/beacon-2.x/"

COPY --from=BUILD /usr/local/lib              /usr/local/lib

RUN groupadd beacon && \
    useradd -M -g beacon beacon && \
    mkdir /beacon

COPY beacon_api /beacon/beacon_api
    
RUN chown -R beacon:beacon /beacon
WORKDIR /beacon
USER beacon
ENTRYPOINT ["python", "-m", "beacon_api"]
