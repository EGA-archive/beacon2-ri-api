"""
Filtering terms Endpoint.

Querying the filtering terms endpoint reveals information about existing ontology filters in this beacon.
These are stored in the DB inside the table named 'ontology_terms'.

.. note:: See ``beacon_api`` root folder ``__init__.py`` for changing values used here.
"""

import logging

from .exceptions import BeaconServerError
from .. import __id__, __beacon_name__, __apiVersion__

LOG = logging.getLogger(__name__)


async def fetch_filtering_terms(db_pool):
    """Execute query for returning the filtering terms.
    """
    # Take one connection from the database pool
    async with db_pool.acquire(timeout=180) as connection:
        # Start a new session with the connection
        async with connection.transaction():
            try:
                query = """SELECT ontology, term, label
                           FROM ontology_term;
                           """
                statement = await connection.prepare(query)
                db_response = await statement.fetch()
                filtering_terms_list = []
                for record in list(db_response):
                    filtering_terms_list.append(dict(record))
                return filtering_terms_list
            except Exception as e:
                raise BeaconServerError(f'Query metadata DB error: {e}')


async def filtering_terms_handler(host, db_pool):
    """Construct the `Beacon` app information dict.
    """
    beacon_filtering_terms = await fetch_filtering_terms(db_pool)

    beacon_answer = {        
        'id': __id__,
        'name': __beacon_name__,
        'apiVersion': __apiVersion__,
        'ontologyTerms': beacon_filtering_terms,
    }

    return beacon_answer
