################################################
##
## Makefile for Local development
##
################################################
SHELL := /bin/bash
TARGET ?= egarchive/beacon
COMMIT ?= latest
CONTAINER ?= beacon

.PHONY: build run exec down server

all: build run server

build:
	docker build $(ARGS) -t $(TARGET):$(COMMIT) .

run:
	docker run -d --rm \
               --name $(CONTAINER) \
               -p 5050:5050 \
               -v $(shell pwd)/deploy/beacon/conf.py \
	       -v $(shell pwd)/beacon:/beacon/beacon \
               --entrypoint "/bin/sleep" \
	       $(TARGET):$(COMMIT) \
           1000000000000

exec:
	docker exec -it $(CONTAINER) bash
server:
	docker exec -it $(CONTAINER) python -m beacon

down:
	-docker kill $(CONTAINER)
	-docker rm $(CONTAINER)
