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

run: ENTRYPOINT=--entrypoint "/bin/sleep"
run: CMD=1000000000000
up run:
	docker run -d --rm \
               --name $(CONTAINER) \
               -p 5050:5050 \
               -v $(shell pwd)/deploy/conf.py:/beacon/beacon/conf.py \
	       -v $(shell pwd)/beacon:/beacon/beacon \
               $(ENTRYPOINT) $(IMG):$(TARGET) $(CMD)

exec:
	docker exec -it $(CONTAINER) bash
server:
	docker exec -it $(CONTAINER) python -m beacon

down:
	-docker kill $(CONTAINER)
	-docker rm $(CONTAINER)
