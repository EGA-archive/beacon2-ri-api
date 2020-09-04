# Deploy with Docker and Docker-Compose

## Getting the code

We have a database file in [LFS](https://git-lfs.github.com/) (Large File Storage), so you first need to [install git-lfs](https://git-lfs.github.com/). After that, you can run the following commands, to get the repository's content, and install the LFS hooks.

	git clone https://github.com/EGA-archive/beacon-2.x.git beacon
	cd beacon
	git lfs install

## Docker Images

We use a [postgres image](https://github.com/docker-library/postgres/blob/34df4665bfdccf28deac2ed2924127b94489a576/9.6/alpine/Dockerfile), for the database, and separate images for the Beacon, the (fake) permissions server and the identity provider.

If you instantiate directly the containers, the images will be automatically downloaded.

If you are not on the master branch, you should (re-)create the images for the Beacon locally. Run the following command in the current directory:

	docker-compose build beacon
	

## Instanciating the beacon database container

At boot time, the database pre-loads some data from the `Genome in a bottle` project.
This takes only a few seconds. Instantiate a container with

	docker-compose up -d db

You can look at what is happening in the container with `docker-compose logs -f db`.

# Dealing with the network for a local deployment

We can point the web browser to `localhost`, on some given port,
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

> The pre-configured settings assume the above.

# Instantiating the other containers 

We have already adjusted the [settings](beacon.yml) for the network and the different connection parameters.

	docker-compose up -d

The beacon is now ready. You can query it on `beacon` (port 5050). For example:  

* [/api](http://beacon:5050/api)
* [/api/g_variants?assemblyId=GRCh37.p1&referenceName=MT&referenceBases=T&alternateBases=C&start=150&includeDatasetResponses=ALL](http://beacon:5050/api/g_variants?assemblyId=GRCh37.p1&referenceName=MT&referenceBases=T&alternateBases=C&start=150&includeDatasetResponses=ALL)
* [/api/g_variants?assemblyId=GRCh37.p1&referenceName=MT&start=1&end=200](http://beacon:5050/api/g_variants?assemblyId=GRCh37.p1&referenceName=MT&start=1&end=200)
* [/api/biosamples](http://beacon:5050/api/biosamples)

and point you browser to [beacon:5050](http://beacon:5050) for the UI.


## Logs

The `-d` flag runs the containers _detached_, ie we get the prompt back. You can check the logs with:

	docker-compose logs -f

## Tear down the demo

Tear down the system and remove the database volume, with:

	docker-compose down -v


## Identity Provider

We use [Keycloak in a container](https://registry.hub.docker.com/r/jboss/keycloak), connected to a Postgres database.
We import a [pre-configured realm](beacon-realm.json), with a beacon client and 2 users:

| Username | Password    | Email                   |
|----------|-------------|-------------------------|
| admin    | secret      |                         |
| john     | john        | john.smith@beacon.ga4gh |
| jane     | jane        | jane.smith@beacon.ga4gh |

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

