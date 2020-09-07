import logging

from aiohttp_session import get_session

from ..utils.exceptions import BeaconBadRequest
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import (RegexField,
                                 ChoiceField,
                                 IntegerField,
                                 ListField)
from ..utils import resolve_token
from ..utils.stream import json_stream
from ..utils import db
from ..utils.json import jsonb

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class Parameters(RequestParameters):
    pass
    #hello = ChoiceField("hi", "salut", "hola", required=True)
    datasets = ListField(default=[])
    #individualSchemas = ListField(items=ChoiceField("ga4gh-phenopacket-individual-v0.1"), default=[])

proxy = Parameters()

async def handler(request):

    qparams_raw, qparams_db = await proxy.fetch(request)

    # print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy, LOG)

    # response = dict(qparams_raw)
    # from decimal import Decimal
    # response['decimal'] = Decimal(1) / Decimal(7)

    response = list([record async for record in db.test()])

    # response = []
    # i = 1
    # async for record in db.test():
    #     LOG.debug('Record %i: %s', i, record)
    #     #r = {}
    #     for key,value in record.items():
    #         LOG.debug("key (%s): %s", type(key), key)
    #         LOG.debug("value (%s): %s", type(value), value)
    #         #r[key] = value
    #     response.append(record)
    #     i+=1

    # Both in one: check the session, and if no session, check the header
    session = await get_session(request)
    token = session.get('access_token')
    if not token:
        LOG.debug('No session token, checking the header')
        token = request.headers.get('Authorization')
        if token:
            LOG.debug('Got a header token')
            token = token[7:].strip() # 7 = len('Bearer ')

    authorized_datasets, authenticated = await resolve_token(token, qparams_db.datasets)


    response['authorized_datasets'] = authorized_datasets
    response['authenticated'] = authenticated

    # return response
    return await json_stream(request, response)

