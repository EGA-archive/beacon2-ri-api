"""
Datasets Endpoint.

Querying the datasets endpoint reveals information about existing datasets in this beacon.

.. note:: See ``beacon_api`` root folder ``__init__.py`` for changing values used here.
"""

import logging

from .exceptions import BeaconServerError
from .. import __id__, __beacon_name__, __apiVersion__

LOG = logging.getLogger(__name__)

def shape_dataset(dataset_record):
    """Shape dataset record into spec dictionary
    """
    authorized = "true" if dataset_record.get("access_type") == 'PUBLIC' else ""
    dataset = {
        "defaultSchema": {
          "version": "beacon-dataset-v0.1",
          "value": {
            "id": dataset_record.get("id"),
            "name": dataset_record.get("stable_id"),
            "description": dataset_record.get("description"),
            "assemblyId": dataset_record.get("reference_genome"),
            "createDateTime": dataset_record.get("create_date_time"),
            "updateDateTime": dataset_record.get("update_date_time"),
            "dataUseConditions": dataset_record.get("data_use_conditions"),
            "version": dataset_record.get("version"),
            "variantCount": dataset_record.get("variant_cnt"),
            "callCount": dataset_record.get("call_cnt"),
            "sampleCount": dataset_record.get("sample_cnt"),
            "externalURL": dataset_record.get("external_url"),
            "info": {
              "accessType": dataset_record.get("access_type"),
              "authorized": authorized
            }
          }
        },
        "alternativeSchemas": []
      }
    return dataset

async def fetch_datasets(db_pool):
    """Execute query for returning the datasets information.
    """
    # Take one connection from the database pool
    async with db_pool.acquire(timeout=180) as connection:
        # Start a new session with the connection
        async with connection.transaction():
            try:
                query = """SELECT *
                           FROM beacon_dataset_table;
                           """
                statement = await connection.prepare(query)
                db_response = await statement.fetch()
                datasets_list = []
                if db_response:
                    for record in list(db_response):
                        datasets_list.append(shape_dataset(dict(record)))
                return datasets_list
            except Exception as e:
                raise BeaconServerError(f'Query metadata DB error: {e}')


async def datasets_handler(host, db_pool):
    """Construct the `Beacon` app information dict.
    """
    beacon_datasets = await fetch_datasets(db_pool)

    beacon_answer = {
                     "meta": {
                        "beaconId": __id__,
                        "apiVersion": __apiVersion__,
                        "receivedRequest": {
                        "meta": {
                            "requestedSchemas": {},
                            "apiVersion": None
                        },
                        "query": {}
                        },
                        "returnedSchemas": {
                        "Dataset": [
                            "beacon-dataset-v0.1"
                            ]
                        }
                    },
                    "response": {
                        "exists": "true" if beacon_datasets else "false",
                        "results": beacon_datasets,
                        "info": None,
                        "resultsHandover": None,
                        "beaconHandover": None
                    }
                }
    return beacon_answer
