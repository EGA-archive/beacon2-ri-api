"""
Info Endpoint.

Querying the info endpoint reveals information about this beacon and its existing datasets 
and their associated metadata.

* ``/`` Beacon-v1
* ``/info`` Beacon-v1
* ``/info?model=GA4GH-ServiceInfo-v0.1`` GA4GH
* ``/service-info`` GA4GH

"""

import logging

from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import ChoiceField, SchemasField, RegexField
from ..utils.db import fetch_datasets_metadata
from ..utils.response import json_stream
from ..response.info_response_schema import build_beacon_response, build_service_info_response
from ..schemas import alternative


LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class InfoParameters(RequestParameters):
    model = ChoiceField('ga4gh-service-info-v1.0', default=None)
    # requested schemas
    requestedSchemasServiceInfo = SchemasField()
    requestedSchemasDataset = SchemasField()
    apiVersion = RegexField(r'^v[0-9]+(\.[0-9]+)*$')


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

proxy_info = InfoParameters()


async def handler(request):
    LOG.info('Running a GET info request')
    _, qparams_db = await proxy_info.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy_info, LOG)

    LOG.debug('model %s', qparams_db.model)
    if qparams_db.model is not None:
        return await handler_ga4gh_service_info(request)

    # Fetch datasets info
    beacon_datasets = [r async for r in fetch_datasets_metadata()]

    response_converted = build_beacon_response(beacon_datasets, qparams_db, build_service_info_response)
    return await json_stream(request, response_converted)


async def handler_ga4gh_service_info(request):
    LOG.info('Running a GET service-info request')

    return await json_stream(request, alternative.ga4gh_service_info_v10(None))


async def prepare_response(qparams_db, request, response, response_type):

    rows = [row async for row in response]
    # build_beacon_response knows how to loop through it
    response_converted = build_beacon_response(rows, qparams_db, response_type)
    return await json_stream(request, response_converted)