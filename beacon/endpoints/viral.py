import logging

from ..utils.response import json_stream
from ..utils.db import fetch_viral_variants_only, fetch_viral_biosamples
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

gvariant_proxy = GVariantParameters()

async def handler_biosamples(request):

    LOG.info('Running a viral biosamples by gvariant request')
    _, qparams_db = await gvariant_proxy.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, gvariant_proxy, LOG)

    response = fetch_viral_biosamples(qparams_db, variant_id=qparams_db.targetIdReq)

    return await prepare_response(qparams_db, request, response, build_biosample_response,
                                  int(qparams_db.targetIdReq) if qparams_db.targetIdReq is not None else None)


async def handler_gvariants(request):

    LOG.info('Running a viral gvariant request')
    _, qparams_db = await gvariant_proxy.fetch(request)

    # print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, gvariant_proxy, LOG)

    if qparams_db.targetIdReq is not None: # by ID
        response = fetch_viral_variants_only(variant_id=qparams_db.targetIdReq)
    elif qparams_db.end is None: # SNP query
        response = fetch_viral_variants_only(start=qparams_db.start,
                                             reference_bases=qparams_db.referenceBases,
                                             alternate_bases=qparams_db.alternateBases)
    else: # Region query
        response = fetch_viral_variants_only(start=qparams_db.start,
                                             end=qparams_db.end)

    return await prepare_response(qparams_db, request, response, build_variant_response,
                                  int(qparams_db.targetIdReq) if qparams_db.targetIdReq is not None else None)


async def prepare_response(qparams_db, request, response, response_type, variant_id_converted=None):

    rows = [row async for row in response]
    # build_beacon_response knows how to loop through it
    response_converted = build_beacon_response(rows, qparams_db, response_type, variant_id=variant_id_converted)
    return await json_stream(request, response_converted)

