import logging

from aiohttp.web import json_response

from ..api.exceptions import BeaconBadRequest
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import (RegexField,
                                 ChoiceField,
                                 IntegerField,
                                 ListField,
                                 DatasetsField)

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class Parameters(RequestParameters):
    hello = ChoiceField("hi", "salut", "hola")
    datasets = DatasetsField()

proxy = Parameters()

async def handler(request):

    qparams_raw, qparams_db = await proxy.fetch(request)

    # print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy, LOG)

    response = dict(qparams_raw)

    return json_response(response)



# access_token = "eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJqb3JkaS5yYW1ibGFAY3JnLmV1IiwiYXpwIjoiY2xpZW50IiwiaXNzIjoiaHR0cHM6XC9cL2lkcC5lZ2EtYXJjaGl2ZS5vcmdcLyIsImV4cCI6MTU4NzE2NDA0MSwiaWF0IjoxNTg3MTYwNDQyLCJqdGkiOiJlYjc0MmQzZS00YmU4LTRkOGItOGRjYS1mYmEzNmE0YjBkOTgifQ.UIOIqAwBN9JuNaeGRB-qxyjZJth-pw0Luyv0vC-pKVl6eraJ3k-3TEcC1CddpNXJu1gT1lCqcW_JecHDzyvymTLtGl6oJb3CAlVGmw1NECCTHShMBpvFQOx2_KkNpKR8z7cAsjcHmzkFdrD9QDp65bPQTRm4imAknJS1G98mf5U5NiKbp0zDiE1WdHfDI7zomKHwmWrNDqvnoTdzzGElRMQWIIB-fiAx3sZPGNGCif2pKOMv1Tk64Qz2Yt8y40U6VFq55N7XBpUtsv8Z0scBaOgiqe_JC0f5hCpi_DeEHUmjnd2hwjMNZmjObNjtqQ_UhmL1ucy8FJD0X5Yh5czVJQ"
