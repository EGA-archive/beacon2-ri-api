# Deployment instructions

## Prerequisites

You should have installed:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [MongoDB Database Tools](https://www.mongodb.com/docs/database-tools/installation/installation/) (specifically `mongoimport` to add the dummy data to the database)
- [Python 3](https://www.python.org/downloads/)

## Installation

All of the commands should be executed from the deploy directory.

```bash
cd deploy
```

### Light up the database

#### Up the DB

```bash
docker-compose up -d db
docker-compose up -d mongo-express
```

With `mongo-express` we can see the contents of the database at [http://localhost:8081](http://localhost:8081).

#### Load the data

To load the database we execute the following commands:

```bash
mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/analyses*.json --collection analyses
mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/biosamples*.json --collection biosamples
mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/cohorts*.json --collection cohorts
mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/datasets*.json --collection datasets
mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/individuals*.json --collection individuals
mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/runs*.json --collection runs
mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file data/genomicVariations*.json --collection genomicVariations
```

This loads the JSON files inside of the `data` folder into the MongoDB database.

> You can also use `make load` as a convenience alias.

#### Create the indexes

You can create the necessary indexes running the following Python script:

```bash
# Install the dependencies
pip3 install pymongo

python3 reindex.py
```

#### Extract the filtering terms

To automatically extract the filtering terms from the data in the database, you can use the following utility script:

```bash
# Install the dependencies
pip3 install pymongo tqdm owlready2 progressbar

python3 extract_filtering_terms.py
```

#### Automatically fetch the ontologies

> This step might require a bit of tinkering since some ontologies used in the dummy data will fail to loaded. I recommend skipping this step unless you know what you are doing.

You can automatically fetch the ontologies that the database is using with the following script:

```bash
# Install the dependencies
pip3 install pymongo tqdm

mkdir ontologies
python3 fetch_ontologies.py
```

### Light up the beacon

#### Up the beacon

Once the database is setup, you can up the beacon with the following command:

```bash
docker-compose up -d beacon
```

#### Check the logs

Check the logs until the beacon is ready to be queried:

```bash
docker-compose logs -f beacon
```
