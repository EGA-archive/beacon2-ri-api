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
    ontology_terms = [
        {
            'id': record['ontology'] + ':' + record['term'],
            'label': record['label']
        }
        async for record in fetch_filtering_terms()]
    response = {
        'beaconId': conf.beacon_id,
        'apiVersion': conf.api_version,
        'filteringTerms': ontology_terms,
    }
    return await json_stream(request, response)
