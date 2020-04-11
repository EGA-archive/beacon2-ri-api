"""
Info Endpoint.

Querying the info endpoint reveals information about this beacon and its existing datasets 
and their associated metadata.

* ``/`` Beacon-v1
* ``/info`` Beacon-v1
* ``/info?model=GA4GH-ServiceInfo-v0.1`` GA4GH
* ``/service-info`` GA4GH

.. note:: See ``beacon_api`` root folder ``__init__.py``  and  ``/utils/models.py`` for changing values used here.
"""

import logging

from aiohttp.web import json_response

from ..api.exceptions import BeaconBasicBadRequest

from ..api.models import GA4GH_ServiceInfo_v01, Beacon_v1, organization, sample_allele_requests

from ..utils.polyvalent_functions import filter_response
from ..api.access_levels import ACCESS_LEVELS_DICT
from ..utils.translate2accesslevels import info2access

from ..utils.validate import parse_request_object
from ..utils.db import fetch_datasets_metadata

LOG = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
#                                         FORMATTING
# ----------------------------------------------------------------------------------------------------------------------

def _transform_metadata(response):
    """Format the metadata record we got from the database to adhere to the response schema."""

    access_type = response.get("accessType")

    return {
        "id": response.get("datasetId"),
        "name": None,
        "variantCount": response.get("variantCount"),
        "callCount": response.get("callCount"),
        "sampleCount": response.get("sampleCount"),
        "createDateTime": None,
        "updateDateTime": None,
        "dataUseConditions": None,
        "version": None,
        "externalURL": None,
        "info": {"accessType": access_type,
                 "authorized": 'true' if access_type == "PUBLIC" else 'false'},
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
    filtered_response = filter_response(beacon_response, ACCESS_LEVELS_DICT, accessible_datasets, user_levels, info2access)

    return filtered_response["beacon"]


async def handler_root(request):
    LOG.info('GET request to the info endpoint.')
    beacon_datasets = [d async for d in fetch_datasets_metadata()]
    response = _finalize(Beacon_v1, beacon_datasets)
    return json_response(response)


async def handler_info(request):
    LOG.info('GET request to the info endpoint.')
    model = request.rel_url.query.get("model")
    if model is None:
        return await handler_root(request)

    # Otherwise, it must be 'GA4GH-ServiceInfo-v0.1', by validation
    beacon_datasets = [d async for d in fetch_datasets_metadata()]
    response = _finalize(GA4GH_ServiceInfo_v01, beacon_datasets)
    return json_response(response)


async def handler_service_info(request):
    LOG.info('GET request to the info endpoint.')
    beacon_datasets = [d async for d in fetch_datasets_metadata()]
    response = _finalize(GA4GH_ServiceInfo_v01, beacon_datasets)
    return json_response(response)

