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
    start = IntegerField(min_value=0)
    end = IntegerField(min_value=0)
    startMin = IntegerField(min_value=0)
    startMax = IntegerField(min_value=0)
    endMin = IntegerField(min_value=0)
    endMax = IntegerField(min_value=0)
    referenceBases = RegexField(r'^([ACGTN]+)$', required=True)
    alternateBases = RegexField(r'^([ACGTN]+)$')
    variantType = ChoiceField("DEL", "INS", "DUP", "INV", "CNV", "SNP", "MNP", "DUP:TANDEM", "DEL:ME", "INS:ME", "BND")
    filters = ListField(items=RegexField(r'.*:.+=?>?<?[0-9]*$'))
    
    def correlate(self, values):
        # values is a namedtuple, with the above keys

        LOG.info('Further correlation for the query endpoint')
        if not values.variantType and not values.alternateBases:
            raise BeaconBadRequest("Either 'alternateBases' or 'variantType' is required")

        if values.variantType and values.alternateBases != "N":
            raise BeaconBadRequest("If 'variantType' is provided then 'alternateBases' must be empty or equal to 'N'")

        if not values.start:
            if values.end:
                raise BeaconBadRequest("'start' is required if 'end' is provided")
            elif not values.startMin and not values.startMax and not values.endMin and not values.endMax:
                raise BeaconBadRequest("Either 'start' or all of 'startMin', 'startMax', 'endMin' and 'endMax' are required")
            elif not values.startMin or not values.startMax or not values.endMin or not values.endMax:
                raise BeaconBadRequest("All of 'startMin', 'startMax', 'endMin' and 'endMax' are required")
        else:
            if values.startMin or values.startMax or values.endMin or values.startMax:
                raise BeaconBadRequest("'start' cannot be provided at the same time as 'startMin', 'startMax', 'endMin' and 'endMax'")
            if not values.end and values.referenceBases == "N":
                raise BeaconBadRequest("'referenceBases' cannot be 'N' if 'start' is provided and 'end' is missing")

        if values.variantType != 'BND' and values.end and values.end < values.start:
            raise BeaconBadRequest("'end' must be greater than 'start'")
        if values.endMin and values.endMin > values.endMax:
            raise BeaconBadRequest("'endMin' must be smaller than 'endMax'")
        if values.startMin and values.startMin > values.startMax:
            raise BeaconBadRequest("'startMin' must be smaller than 'startMax'") 


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
