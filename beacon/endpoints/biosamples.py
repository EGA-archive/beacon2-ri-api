import logging

from ..api.response import json_stream
from ..api.db import fetch_viral_variants_only, fetch_viral_biosamples
from ..validation.request import print_qparams
from ..validation.common_parameter_validation import GVariantParameters
from ..response.response_schema import build_beacon_response, build_variant_response, build_biosample_response

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

biosample_gvariant_proxy = GVariantParameters()

async def handler_gvariants(request):

    LOG.info('Running a viral gvariant by biosample request')
    _, qparams_db = await biosample_gvariant_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, biosample_gvariant_proxy, LOG)

    response = fetch_viral_variants_only(biosample_stable_id=qparams_db.targetIdReq)

    return await prepare_response(qparams_db, request, response, build_variant_response, qparams_db.targetIdReq)


async def handler(request):

    LOG.info('Running a viral biosample request')
    _, qparams_db = await biosample_gvariant_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, biosample_gvariant_proxy, LOG)

    response = fetch_viral_biosamples(qparams_db, biosample_stable_id=qparams_db.targetIdReq)
    return await prepare_response(qparams_db, request, response, build_biosample_response, qparams_db.targetIdReq)


async def prepare_response(qparams_db, request, response, response_type, biosample_id=None):

    rows = [row async for row in response]
    # build_beacon_response knows how to loop through it
    response_converted = build_beacon_response(rows, qparams_db, response_type, biosample_id=biosample_id)
    return await json_stream(request, response_converted)

