"""
Filtering terms Endpoint.

Querying the filtering terms endpoint reveals information about existing ontology filters in this beacon.
These are stored in the DB inside the table named 'ontology_terms'.

"""

# import logging

from ... import conf
from ...utils.db import fetch_filtering_terms
from ...utils.stream import json_stream

# LOG = logging.getLogger(__name__)

async def handler(request):
    ontologyTerms = [record async for record in fetch_filtering_terms()]
    response = {
        'id': conf.beacon_id,
        'name': conf.beacon_name,
        'apiVersion': conf.api_version,
        'ontologyTerms': ontologyTerms,
    }
    return await json_stream(request, response)
