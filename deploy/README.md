# Deploy with Docker and Docker-Compose

## Docker Images

We use a [postgres image](https://github.com/docker-library/postgres/blob/34df4665bfdccf28deac2ed2924127b94489a576/9.6/alpine/Dockerfile), for the database, and 2 separate images for the Beacon and the Beacon UI.

If you instantiate directly the containers, the images will be automatically downloaded.

If you prefer to (re-)create the images for the Beacon and Beacon UI locally, run the following command in the current directory:

	docker-compose build beacon ui
	

## Instanciating the containers

At boot time, the database pre-loads some data from the `1000 genomes` project.
This takes only a few seconds. Instantiate a container with

	docker-compose up -d db

You can look at what is happening in the container with `docker-compose logs -f db`.

Once ready, you can now instanciate the other containers. We have already adjusted the [settings](beacon.yml) for the network and the different connection parameters.

	docker-compose up -d beacon

The beacon is now ready. You can query it on `localhost` (port 5050). For example:  

* [localhost:5050/](http://localhost:5050/)
* [localhost:5050/query?referenceName=Y&start=2655179&referenceBases=G&alternateBases=A&assemblyId=GRCh37&datasetIds=1000genomes](http:/localhost:5050/query?referenceName=Y&start=2655179&referenceBases=G&alternateBases=A&assemblyId=GRCh37&datasetIds=1000genomes)
* [localhost:5050/query?referenceName=Y&start=2655179&referenceBases=G&alternateBases=A&assemblyId=GRCh37&datasetIds=1000genomes&includeDatasetResponses=HIT](http:/localhost:5050/query?referenceName=Y&start=2655179&referenceBases=G&alternateBases=A&assemblyId=GRCh37&datasetIds=1000genomes&includeDatasetResponses=HIT)

Finally, you can new start the Beacon UI with:

	docker-compose up -d ui

and point you browser to [localhost:8000](http://localhost:8000)


## Logs

The `-d` flag runs the containers _detached_, ie we get the prompt back. You can check the logs with:

	docker-compose logs -f

## Tear down the demo

Tear down the system and remove the database volume, with:

	docker-compose down -v


## Identity Provider

We use [Keycloak in a container](https://registry.hub.docker.com/r/jboss/keycloak), connected to a Postgres database.
We import a [pre-configured realm](beacon-realm.json), with a beacon client and 4 users:

| Username | Password    | Email                   |
|----------|-------------|-------------------------|
| admin    | secret      |                         |
| john     | john        | john.smith@beacon.ga4gh |
| jane     | jane        | jane.smith@beacon.ga4gh |
| sabela   | ihatefred   | sabela.delatorre@crg.eu |
| fred     | ihatesabela | frederic.haziza@crg.eu  |
