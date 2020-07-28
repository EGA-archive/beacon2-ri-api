import logging

from ..utils.response import json_stream
from ..utils.db import fetch_variants, fetch_biosamples, fetch_individuals
from ..validation.request import print_qparams
from ..validation import GVariantParameters
from ..response.response_schema import build_beacon_response, build_variant_response, build_biosample_response, build_individual_response

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

biosample_gvariant_proxy = GVariantParameters()

async def handler_gvariants(request):

    LOG.info('Running a gvariant by biosample request')
    await generic_biosample_handler(request, fetch_variants, build_variant_response)


async def handler_individuals(request):

    LOG.info('Running an individual by biosample request')
    await generic_biosample_handler(request, fetch_individuals, build_individual_response)


async def handler_biosamples(request):
    LOG.info('Running a biosample request')
    await generic_biosample_handler(request, fetch_biosamples, build_biosample_response)


async def generic_biosample_handler(request, fetch_function, build_response_type):

    _, qparams_db = await biosample_gvariant_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, biosample_gvariant_proxy, LOG)

    LOG.debug('qparams_db.targetIdReq= %s', qparams_db.targetIdReq)

    response = fetch_function(qparams_db, biosample_stable_id=qparams_db.targetIdReq)
    return await prepare_response(qparams_db, request, response, build_response_type, qparams_db.targetIdReq)


async def prepare_response(qparams_db, request, response, response_type, biosample_id=None):

    rows = [row async for row in response]
    # build_beacon_response knows how to loop through it
    response_converted = build_beacon_response(rows, qparams_db, response_type, biosample_id=biosample_id)
    return await json_stream(request, response_converted)

