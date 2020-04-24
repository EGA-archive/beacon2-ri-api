import logging

from ..api.response import beacon_response
from ..api.db import fetch_viral
from ..api.exceptions import BeaconBadRequest
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import (RegexField,
                                 ChoiceField,
                                 IntegerField,
                                 ListField)

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class Parameters(RequestParameters):
    start = IntegerField(min_value=0, required=True)
    end = IntegerField(min_value=0)
    referenceBases = RegexField(r'^([ACGT]+)$', required=True)
    alternateBases = RegexField(r'^([ACGT]+)$', required=True)
    offset = IntegerField(min_value=0, default=0)
    limit = IntegerField(min_value=0, default=10)
    
    def correlate(self, values):
        # values is a namedtuple, with the above keys
        LOG.info('Further correlation for the query endpoint')
        if values.end and values.start > values.end:
            raise BeaconBadRequest("Come on... 'start < end'")


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

proxy = Parameters()

async def handler(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given QUERY.
    It uses the '/query' path and expects some parameters.
    """
    LOG.info('Running a query request')
    qparams_raw, qparams_db = await proxy.fetch(request)
    LOG.debug("Original Query Parameters: %s", qparams_raw)

    # print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy, LOG)

    # Fetch info from the database. It returns an async gen
    # beacon_response knows how to loop through it
    response = fetch_viral(qparams_db)

    return await beacon_response(request, response)
