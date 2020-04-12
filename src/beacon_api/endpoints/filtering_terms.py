"""
Filtering terms Endpoint.

Querying the filtering terms endpoint reveals information about existing ontology filters in this beacon.
These are stored in the DB inside the table named 'ontology_terms'.

.. note:: See ``beacon_api`` root folder ``__init__.py`` for changing values used here.
"""

import logging

from aiohttp.web import json_response

from .. import conf
from ..utils.db import fetch_filtering_terms


LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def handler(request):
    """Construct the `Beacon` app information dict.
    """
    beacon_filtering_terms = [dict(record) async for record in fetch_filtering_terms()]

    response = {
        'id': conf.beacon_id,
        'name': conf.beacon_name,
        'apiVersion': conf.api_version,
        'ontologyTerms': beacon_filtering_terms,
    }

    return json_response(response)
