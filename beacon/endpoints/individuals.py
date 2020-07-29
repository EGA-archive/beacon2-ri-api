import logging

from ..utils.response import json_stream
from ..utils.db import fetch_variants, fetch_individuals, fetch_biosamples
from ..validation.request import print_qparams
from ..validation import GVariantParameters
from ..response.response_schema import build_beacon_response, build_variant_response, build_individual_response, build_biosample_response

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

individual_gvariant_proxy = GVariantParameters()

async def handler_gvariants(request):

    LOG.info('Running a gvariant by individual request')
    await generic_individual_handler(request, fetch_variants, build_variant_response)
    # _, qparams_db = await individual_gvariant_proxy.fetch(request)
    #
    # if LOG.isEnabledFor(logging.DEBUG):
    #     print_qparams(qparams_db, individual_gvariant_proxy, LOG)
    #
    # response = fetch_variants(ind=qparams_db.targetIdReq)
    #
    # return await prepare_response(qparams_db, request, response, build_variant_response, qparams_db.targetIdReq)


async def handler_biosamples(request):

    LOG.info('Running a biosamples by individual request')
    await generic_individual_handler(request, fetch_biosamples, build_biosample_response)


async def handler_individuals(request):

    LOG.info('Running an individual request')
    await generic_individual_handler(request, fetch_individuals, build_individual_response)


async def generic_individual_handler(request, fetch_function, build_response_type):

    _, qparams_db = await individual_gvariant_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, individual_gvariant_proxy, LOG)

    LOG.debug('qparams_db.targetIdReq= %s', qparams_db.targetIdReq)

    response = fetch_function(qparams_db, individual_stable_id=qparams_db.targetIdReq)
    return await prepare_response(qparams_db, request, response, build_response_type, qparams_db.targetIdReq)


async def prepare_response(qparams_db, request, response, response_type, individual_id=None):

    rows = [row async for row in response]
    # build_beacon_response knows how to loop through it
    response_converted = build_beacon_response(rows, qparams_db, response_type, individual_id=individual_id)
    return await json_stream(request, response_converted)

