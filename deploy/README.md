# Deployment instructions

[![](https://mermaid.ink/img/pako:eNp1U01vgzAM_Ssop01qdtiRw6RRWm1SD91WJk2lhxRMGw0SFEg_VvW_z4EE2pX15Lz3bD_b9EQSmQLxyUaxcuvN3mPh4S-qQC0z5meMagyb98pSr5bYc5HKPS3YgRf8B5Cwiue5k2DWDrNfFou5QS0fBneWT1nN1qwCL7TB6j4WVoTI8ktq5RmRzRzLotR1Zy2F6ruWZQdb1eSQQG4lGc-BggFa2Eo-x1NXQzDzsngwnV4kmufKGar0ut3RmwZ1bDG3Ko_SJ5y_B52jhsDJe6aPuoJrYIkU9PHh0JN2j01-GFzjYXBbFkTqjA7VrhXjgosN1fy6VvR_jei2u-0cDc5j9WYfPehmcAtpmYtOnVNzcG8mWYo2Lzoa1BRorjc0YJbRHcs5fiVSXc_WpDTJeMfBTeLhHf9nDTYgI1KAKhhP8S9yMnBM6i0UEBMfQwEaN5vHJBZnlOoSXcAk5WiF-LXSMCJM1_LjKBL3bjUhZ2i_aMHzL0zOAvw)](https://mermaid.live/edit#pako:eNp1U01vgzAM_Ssop01qdtiRw6RRWm1SD91WJk2lhxRMGw0SFEg_VvW_z4EE2pX15Lz3bD_b9EQSmQLxyUaxcuvN3mPh4S-qQC0z5meMagyb98pSr5bYc5HKPS3YgRf8B5Cwiue5k2DWDrNfFou5QS0fBneWT1nN1qwCL7TB6j4WVoTI8ktq5RmRzRzLotR1Zy2F6ruWZQdb1eSQQG4lGc-BggFa2Eo-x1NXQzDzsngwnV4kmufKGar0ut3RmwZ1bDG3Ko_SJ5y_B52jhsDJe6aPuoJrYIkU9PHh0JN2j01-GFzjYXBbFkTqjA7VrhXjgosN1fy6VvR_jei2u-0cDc5j9WYfPehmcAtpmYtOnVNzcG8mWYo2Lzoa1BRorjc0YJbRHcs5fiVSXc_WpDTJeMfBTeLhHf9nDTYgI1KAKhhP8S9yMnBM6i0UEBMfQwEaN5vHJBZnlOoSXcAk5WiF-LXSMCJM1_LjKBL3bjUhZ2i_aMHzL0zOAvw)

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

### Light up the database and the Beacon

#### Up the docker network

```bash
docker network create my-app-network
```

#### Up the containers

If you are using a build with all the services in the same cluster, you can use:

```bash
docker-compose up -d --build
```

If you are willing to deploy every service in a different environment from the other services, you can use:

```bash
docker-compose -f docker-compose.remote.yml up -d --build
```

With `mongo-express` we can see the contents of the database at [http://localhost:8081](http://localhost:8081).

#### Load the data

To load the database we execute the following commands:

```bash
docker cp /path/to/analyses.json rimongo:tmp/analyses.json
docker cp /path/to/biosamples.json rimongo:tmp/biosamples.json
docker cp /path/to/cohorts.json rimongo:tmp/cohorts.json
docker cp /path/to/datasets.json rimongo:tmp/datasets.json
docker cp /path/to/genomicVariations.json rimongo:tmp/genomicVariations.json
docker cp /path/to/individuals.json rimongo:tmp/individuals.json
docker cp /path/to/runs.json rimongo:tmp/runs.json
```

```bash
docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/datasets.json --collection datasets
docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/analyses.json --collection analyses
docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/biosamples.json --collection biosamples
docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/cohorts.json --collection cohorts
docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/genomicVariations.json --collection genomicVariations
docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/individuals.json --collection individuals
docker exec rimongo mongoimport --jsonArray --uri "mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin" --file /tmp/runs.json --collection runs
```

This loads the JSON files inside of the `data` folder into the MongoDB database container. Each time you import data you will have to create indexes for the queries to run smoothly. Please, check the next point about how to Create the indexes.

#### Create the indexes

Remember to do this step every time you import new data!!

You can create the necessary indexes running the following Python script:

```bash
docker exec beacon python beacon/reindex.py
```

#### List the ids

After deploying all the data, you will need to tell the beacon which are the individual and biosample ids belonging to each dataset and cohort. In order to do that, please, add the name of each dataset with the respective array of all the ids together in this file [datasets.yml](../beacon/request/datasets.yml).
Then, repeat the same for the cohorts modifying this file [cohorts.yml](../beacon/request/cohorts.yml).

#### Fetch the ontologies and extract the filtering terms

> This step consists of analyzing all the collections of the Mongo database for first extracting the ontology OBO files and then filling the filtering terms endpoint with the information of the data loaded in the database.

You can automatically fetch the ontologies and extract the filtering terms running the following script:

```bash
docker exec beacon python beacon/db/extract_filtering_terms.py
```

#### Get descendant and semantic similarity terms

**If you have the ontologies loaded and the filtering terms extracted**, you can automatically get their descendant and semantic similarity terms by following the next two steps:

1. Add your .obo files inside [ontologies](../beacon/db/ontologies) naming them as the ontology prefix in lowercase (e.g. ncit.obo) and rebuild the beacon container with:

2. Run the following script:

```bash
docker exec beacon python beacon/db/get_descendants.py
```

#### Check the logs

Check the logs until the beacon is ready to be queried:

```bash
docker-compose logs -f beacon
```

## Usage

You can query the beacon using GET or POST. Below, you can find some examples of usage:

> For simplicity (and readability), we will be using [HTTPie](https://github.com/httpie/httpie).

### Using GET

Querying this endpoit it should return the 13 variants of the beacon (paginated):

```bash
http GET http://localhost:5050/api/g_variants
```

You can also add [request parameters](https://github.com/ga4gh-beacon/beacon-v2-Models/blob/main/BEACON-V2-Model/genomicVariations/requestParameters.json) to the query, like so:

```bash
http GET http://localhost:5050/api/individuals?filters=NCIT:C16576,NCIT:C42331
```

### Using POST

You can use POST to make the previous query. With a `request.json` file like this one:

```json
{
    "meta": {
        "apiVersion": "2.0"
    },
    "query": {
        "requestParameters": {
    "alternateBases": "G" ,
    "referenceBases": "A" ,
"start": [ 16050074 ],
            "end": [ 16050568 ],
	    "variantType": "SNP"
        },
        "filters": [],
        "includeResultsetResponses": "HIT",
        "pagination": {
            "skip": 0,
            "limit": 10
        },
        "testMode": false,
        "requestedGranularity": "record"
    }
}

```

You can execute:

```bash
curl \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "meta": {
        "apiVersion": "2.0"
    },
    "query": {
        "requestParameters": {
    "alternateBases": "G" ,
    "referenceBases": "A" ,
"start": [ 16050074 ],
            "end": [ 16050568 ],
	    "variantType": "SNP"
        },
        "filters": [],
        "includeResultsetResponses": "HIT",
        "pagination": {
            "skip": 0,
            "limit": 10
        },
        "testMode": false,
        "requestedGranularity": "record"
    }
}' \
  http://localhost:5050/api/g_variants


```

But you can also use complex filters:

```json
{
    "meta": {
        "apiVersion": "2.0"
    },
    "query": {
        "filters": [
            {
                "id": "UBERON:0000178",
                "scope": "biosample",
                "includeDescendantTerms": false
            }
        ],
        "includeResultsetResponses": "HIT",
        "pagination": {
            "skip": 0,
            "limit": 10
        },
        "testMode": false,
        "requestedGranularity": "count"
    }
}
```

You can execute:

```bash
http POST http://localhost:5050/api/biosamples --json < request.json
```

And it will use the ontology filter to filter the results.
