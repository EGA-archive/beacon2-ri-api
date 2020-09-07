import logging

from ...utils import resolve_token
from ...utils.stream import json_stream
from ...utils.db import fetch_variants, fetch_biosamples, fetch_individuals
from ...validation.request import print_qparams
from . import GVariantParameters
from .response.response_schema import (build_beacon_response,
                                       build_variant_response,
                                       build_biosample_response, 
                                       build_individual_response)

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

biosample_gvariant_proxy = GVariantParameters()

async def generic_biosample_handler(request, fetch_function, build_response_type):

    _, qparams_db = await biosample_gvariant_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, biosample_gvariant_proxy, LOG)

    LOG.debug('qparams_db.targetIdReq= %s', qparams_db.targetIdReq)

    access_token = request.headers.get('Authorization')
    if access_token:
        access_token = access_token[7:] # cut out 7 characters: len('Bearer ')

    datasets, authenticated = await resolve_token(access_token, qparams_db.datasetIds)
    if authenticated:
        LOG.debug('requested datasets:  %s', qparams_db.datasetIds)
        LOG.info('resolved datasets:  %s', datasets)

    response = fetch_function(qparams_db, datasets, authenticated, biosample_stable_id=qparams_db.targetIdReq)

    rows = [row async for row in response]

    # build_beacon_response knows how to loop through it
    response_converted = build_beacon_response(rows, qparams_db, build_response_type, biosample_id=qparams_db.targetIdReq)
    return await json_stream(request, response_converted)


async def handler_gvariants(request):

    LOG.info('Running a gvariant by biosample request')
    return await generic_biosample_handler(request, fetch_variants, build_variant_response)


async def handler_individuals(request):

    LOG.info('Running an individual by biosample request')
    return await generic_biosample_handler(request, fetch_individuals, build_individual_response)


async def handler_biosamples(request):

    LOG.info('Running a biosample request')
    return await generic_biosample_handler(request, fetch_biosamples, build_biosample_response)


