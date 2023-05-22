################################################
##
## Makefile for Local development
##
################################################
SHELL := /bin/bash
IMG ?= egarchive/beacon
TARGET ?= 2.0
CONTAINER ?= beacon

.PHONY: build run exec down server

all: build run server

build:
	docker build $(ARGS) -t $(IMG):$(TARGET) .

run: PORTS=-p 5050:5050
up: PORTS=-p 5050:8000
run: ENTRYPOINT=--entrypoint "/bin/sleep"
run: CMD=1000000000000
up run:
	docker run -d --rm \
               --name $(CONTAINER) \
               $(PORTS) \
               -v $(shell pwd)/deploy/conf.py:/beacon/beacon/conf.py \
	       -v $(shell pwd)/beacon:/beacon/beacon \
	       -v $(shell pwd)/ui/static:/beacon/static \
	       -v $(shell pwd)/ui/templates:/beacon/templates \
               $(ENTRYPOINT) $(IMG):$(TARGET) $(CMD)

exec-root: D_USER=--user root
exec-root exec:
	docker exec -it $(D_USER) $(CONTAINER) bash
server:
	docker exec -it $(CONTAINER) python -m beacon

down:
	-docker kill $(CONTAINER)
	-docker rm $(CONTAINER)
