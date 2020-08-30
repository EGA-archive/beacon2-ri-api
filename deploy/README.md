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

Exporting the settings can be done with:

	docker-compose exec idp /opt/jboss/keycloak/bin/standalone.sh \
	-Djboss.socket.binding.port-offset=100 \
	-Dkeycloak.migration.action=export \
	-Dkeycloak.migration.provider=singleFile \
	-Dkeycloak.migration.realmName=Beacon \
	-Dkeycloak.migration.usersExportStrategy=REALM_FILE \
	-Dkeycloak.migration.file=/tmp/export-beacon-realm.json
	
Once it has run, you can stop the above command and copy out the file from the container

	docker cp idp:/tmp/export-beacon-realm.json <destination-path>

# Dealing with the network for a local deployment

We can make our web browser point to `localhost`, on some given port,
which docker will redirect to the relevant container. That part is
fine, but when a docker container A needs to call another container B
using a URL pointing to `localhost`, it will look at itself (ie,
packets don't get out of A), and won't find the service running on the
chosen port.

We cannot circumvent this issue by _adding_ DNS entries, to point to
the other containers. This issue is to change an already existing one
inside the container, namely `localhost`.

A simple solution is to update your local machine's DNS resolution by
adding to `/etc/hosts`, the following entries:

	127.0.0.1      idp
	127.0.0.1      beacon
	127.0.0.1      beacon-permissions

That way, you can make your browser point to `http://idp:8080` and
`http://beacon:5050`, and they'll redirect to the right container. The
same is true from _within_ those containers (because they either
already have a DNS entry, or they don't, would get out of the
container and then use the above newly added entries).
