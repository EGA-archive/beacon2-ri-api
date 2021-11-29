
# Requirements

- Docker
- Docker Compose

# Usage

## Deploy the DB

```sh
docker-compose up -d db
```

Make sure that the database has finished before deploying the beacon. To do that you can check the logs with:

```sh
docker-compose up logs -f db
```

## Deploy the beacon

```sh
docker-compose up -d
```

## Load data into the database

We provide tools to generate the JSON files necessary to load the database.

### Generate JSON files

#### With real data

> Coming soon!

#### With fake data

We can generate any amount of fake data that we want. To do that, we use multiple JSON schema utilities:

- [`json-schema-faker-cli`](https://github.com/oprogramador/json-schema-faker-cli): A JSON schema fake data generator that takes the [Model](https://github.com/ga4gh-beacon/beacon-v2-Models/) and generates fake data for each of the entities.
- [json-dereference-cli](https://github.com/davidkelley/json-dereference-cli): A JSON schema deferencing tool to make the json schema faker generator work properly and faster.

To install both of the utilities, run:

```bash
npm install -g fake-schema-cli
npm install -g json-dereference-cli
```

We provide a small script to make it easy to generate fake data with this utilities.

The script does the following:

- It gets the schemas from the model and framework repositories.
- It removes the `endpoints.json` files since those are OpenAPI files and not schemas.
- It replaces all of the remote references with local references since the repositories have been downloaded already.
- It deferences all of the schemas in the repositories, creating one big `defaultSchema.json` files for each entity.
- Then, it generates all of the fake json files that we will use as placeholder data for the beacon.

To run the script and generate 10 instances for every entity, execute:

```bash
make generate
```

### Load JSON into MongoDB

To load an entity JSON file into the database, execute the following to load every entity:

```sh
make load
```

### MongoDB

> Coming soon!
