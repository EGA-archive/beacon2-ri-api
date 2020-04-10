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

from .exceptions import BeaconBadRequest, BeaconServerError, BeaconBasicBadRequest

from ..utils.models import GA4GH_ServiceInfo_v01, Beacon_v1, organization, sample_allele_request

from ..utils.polyvalent_functions import filter_response
from .access_levels import ACCESS_LEVELS_DICT
from ..utils.translate2accesslevels import info2access

from ..utils import ensure_json_response

LOG = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
#                                         FORMATTING
# ----------------------------------------------------------------------------------------------------------------------

def _transform_metadata(record):
    """Format the metadata record we got from the database to adhere to the response schema."""

    access_type = record.get("accessType")

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
#                                         MAIN QUERY TO THE DATABASE
# ----------------------------------------------------------------------------------------------------------------------

@capture_server_error(prefix='Query metadata DB error: ')
async def fetch_dataset_metadata(db_pool):
    """
    Execute query for returning dataset metadata.

    Returns a list of datasets metadata dictionaries. 
    """
    # Take one connection from the database pool
    async with db_pool.acquire(timeout=180) as connection:
        query = """SELECT stable_id                as "datasetId",
                          description              as "description",
                          access_type                                as "accessType",
                          reference_genome                           as "assemblyId",
                          COALESCE(variant_cnt, 0) as "variantCount",
                          COALESCE(call_cnt   , 0) as "callCount",
                          COALESCE(sample_cnt , 0) as "sampleCount",
                   FROM beacon_dataset;"""
        db_response = await connection.fetch(query)
        for record in db_response:
            yield _transform_metadata(record)


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

def complete_info(beacon_info, beacon_datasets):
    beacon_info.update({'datasets': beacon_datasets,
                        # If one sets up a beacon it is recommended to adjust these sample requests
                        'sampleAlleleRequests': sample_allele_request}) 

    # Before returning the response we need to filter it depending on the access levels
    beacon_response = {"beacon": beacon_info}
    accessible_datasets = []  # NOTE we use the an empty list because in this endpoint we don't filter by dataset
    user_levels = ["PUBLIC"]  # NOTE we hardcode it because authentication is not implemented yet
    filtered_response = filter_response(beacon_response, ACCESS_LEVELS_DICT, accessible_datasets, user_levels, info2access)

    return filtered_response["beacon"]


async def handler_root(request):

    # Fetch the info about the datasets
    beacon_dataset = list(await fetch_dataset_metadata(request['pool']))

    # Decide whether the Beacon_v1 or the GA4GH spec is used (while validating the model parameter)
    # if info, then check the parameter model, if it is passed fine then use GA4GH model, if not, use the default model, which is Beacon-v1
    if info_endpoint:
        if not processed_request:
            LOG.info('Using Beacon API Specification format for Service Info.')
            beacon_info = Beacon_v1(request.host)
        elif processed_request.get("model") and processed_request.get("model") == 'GA4GH-ServiceInfo-v0.1':
            LOG.info('Using GA4GH Discovery format for Service Info.')
            beacon_info = GA4GH_ServiceInfo_v01(request.host)
        else:
            error = "The info endpoint only accepts 'model' as parameter with 'GA4GH-ServiceInfo-v0.1' as value."
            raise BeaconBasicBadRequest(processed_request, request.host, error)


async def handler_service_info(request):

    LOG.info('Using GA4GH Discovery format for Service Info.')

    # Fetch the info about the datasets
    beacon_dataset = list(await fetch_dataset_metadata(request['pool']))

    beacon_info = GA4GH_ServiceInfo_v01(request.host)


@ensure_json_response
async def info_handler(request, processed_request, pool, info_endpoint=False, service_info=False):
    """
    Construct the `Beacon` app information dict.
    Handle in which model the info is output depending on the endpoint and the parameters passed. 

    :info_rendpoint: boolean to decide which response model to use.
    :service_info: boolean to decide which response model to use.

    Returns the beacon response dictionary. 
    """

    # Fetch the info about the datasets
    beacon_dataset = list(await fetch_dataset_metadata(pool))

    # Decide whether the Beacon_v1 or the GA4GH spec is used (while validating the model parameter)
    # if info, then check the parameter model, if it is passed fine then use GA4GH model, if not, use the default model, which is Beacon-v1
    if info_endpoint:
        if not processed_request:
            LOG.info('Using Beacon API Specification format for Service Info.')
            beacon_info = Beacon_v1(request.host)
        elif processed_request.get("model") and processed_request.get("model") == 'GA4GH-ServiceInfo-v0.1':
            LOG.info('Using GA4GH Discovery format for Service Info.')
            beacon_info = GA4GH_ServiceInfo_v01(request.host)
        else:
            error = "The info endpoint only accepts 'model' as parameter with 'GA4GH-ServiceInfo-v0.1' as value."
            raise BeaconBasicBadRequest(processed_request, request.host, error)
    # if there is service_info then use ga4gh
    elif service_info:
        LOG.info('Using GA4GH Discovery format for Service Info.')
        beacon_info = GA4GH_ServiceInfo_v01(request.host)


    beacon_info.update({'datasets': beacon_dataset,
                        # If one sets up a beacon it is recommended to adjust these sample requests
                        'sampleAlleleRequests': sample_allele_request}) 

    # Before returning the response we need to filter it depending on the access levels
    beacon_response = {"beacon": beacon_info}
    accessible_datasets = []  # NOTE we use the an empty list because in this endpoint we don't filter by dataset
    user_levels = ["PUBLIC"]  # NOTE we hardcode it because authentication is not implemented yet
    filtered_response = filter_response(beacon_response, ACCESS_LEVELS_DICT, accessible_datasets, user_levels, info2access)

    return filtered_response["beacon"]

    # return beacon_info
