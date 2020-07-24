import logging

from ..api.exceptions import BeaconBadRequest
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import (RegexField,
                                 ChoiceField,
                                 IntegerField,
                                 ListField,
                                 DatasetsField)
from ..api.response import json_stream

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class Parameters(RequestParameters):
    hello = ChoiceField("hi", "salut", "hola", required=True)
    #datasets = DatasetsField()
    individualSchemas = ListField(items=ChoiceField("ga4gh-phenopacket-individual-v0.1"), default=[])

proxy = Parameters()

async def handler(request):

    qparams_raw, qparams_db = await proxy.fetch(request)

    # print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy, LOG)

    response = dict(qparams_raw)
    from decimal import Decimal
    response['decimal'] = Decimal(1) / Decimal(7)

    # return response
    return await json_stream(request, response)
