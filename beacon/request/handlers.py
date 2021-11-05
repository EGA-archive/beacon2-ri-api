import json
from aiohttp import web
from aiohttp.web_request import Request
from bson import json_util

from beacon.request import get_parameters
from beacon.response.info_response_schema import build_beacon_resultset_response
import logging

LOG = logging.getLogger(__name__)


def generic_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        LOG.debug(type(request))
        qparams = await get_parameters(request)
        entry_id = request.match_info["id"] if "id" in request.match_info else None

        # Get response
        response_converted = [ json.loads(json_util.dumps(r)) for r in db_fn(entry_id, qparams)]
        response = build_beacon_resultset_response(response_converted, len(response_converted), qparams, lambda x, y: x)
        return web.json_response(response)

    return wrapper
