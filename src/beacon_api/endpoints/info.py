"""
Info Endpoint.

Querying the info endpoint reveals information about this beacon and its existing datasets 
and their associated metadata.

* ``/`` Beacon-v1
* ``/info`` Beacon-v1
* ``/info?model=GA4GH-ServiceInfo-v0.1`` GA4GH
* ``/service-info`` GA4GH

.. note:: Update values in ``api/models.py``.
"""

import logging

from aiohttp.web import json_response

from ..api.models import GA4GH_ServiceInfo_v01, Beacon_v1, organization, sample_allele_requests
from ..validation.request import RequestParameters
from ..validation.fields import ChoiceField

# from ..utils.polyvalent_functions import filter_response
# from ..api.access_levels import ACCESS_LEVELS_DICT
# from ..utils.translate2accesslevels import info2access

from ..utils.db import fetch_datasets_metadata

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class RootParameters(RequestParameters):
    pass

class InfoParameters(RequestParameters):
    model = ChoiceField('GA4GH-ServiceInfo-v0.1', required=True)


# ----------------------------------------------------------------------------------------------------------------------
#                                         FORMATTING
# ----------------------------------------------------------------------------------------------------------------------

def record_to_dict(record):
    return {
        "id": record["datasetId"],
        "name": None,
        "exists": True,
        "createDateTime": None,
        "updateDateTime": None,
        "dataUseConditions": None,
        "version": None,
        "variantCount": record["variantCount"], # already coalesced
        "callCount": record["callCount"],
        "sampleCount": record["sampleCount"],
        # "frequency": float(record["frequency"] or 0), # is it ok with 0.0 ?
        # # "frequency": 0 if record["frequency"] is None else float(record["frequency"])
        # No numVariants?
        "externalURL": None,
        "info": { "accessType": record["accessType"],
                  "authorized": 'true' if record["accessType"] == "PUBLIC" else 'false'} 
    }

# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

def _finalize(beacon_info, beacon_datasets):
    beacon_info['datasets'] = beacon_datasets
    # If one sets up a beacon it is recommended to adjust these sample requests
    beacon_info['sampleAlleleRequests'] = sample_allele_requests

    # Before returning the response we need to filter it depending on the access levels
    beacon_response = {"beacon": beacon_info}
    accessible_datasets = []  # NOTE we use the an empty list because in this endpoint we don't filter by dataset
    user_levels = ["PUBLIC"]  # NOTE we hardcode it because authentication is not implemented yet

    return beacon_response
    # filtered_response = filter_response(beacon_response, ACCESS_LEVELS_DICT, accessible_datasets, user_levels, info2access)
    # return filtered_response["beacon"]

proxy_root = RootParameters()
async def handler_root(request):
    LOG.info('GET request to the info endpoint.')
    qparams = await proxy_root.fetch(request) # validate
    beacon_datasets = [r async for r in fetch_datasets_metadata(transform=record_to_dict)]
    response = _finalize(Beacon_v1, beacon_datasets)
    return json_response(response)


proxy_info = InfoParameters()
async def handler_info(request):
    LOG.info('GET request to the info endpoint.')
    model = request.rel_url.query.get("model")
    if model is None:
        return await handler_root(request)

    # Otherwise, it must be 'GA4GH-ServiceInfo-v0.1', by validation
    qparams = await proxy_info.fetch(request) # validate with model=GA4GH-ServiceInfo-v0.1

    beacon_datasets = [r async for r in fetch_datasets_metadata(transform=record_to_dict)]
    response = _finalize(GA4GH_ServiceInfo_v01, beacon_datasets)
    return json_response(response)


async def handler_service_info(request):
    LOG.info('GET request to the info endpoint.')
    beacon_datasets = [r async for r in fetch_datasets_metadata(transform=record_to_dict)]
    response = _finalize(GA4GH_ServiceInfo_v01, beacon_datasets)
    return json_response(response)

