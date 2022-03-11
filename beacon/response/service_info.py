import logging
from aiohttp.web_request import Request
from beacon.response.build_response import build_beacon_service_info_response
from beacon.utils.stream import json_stream

LOG = logging.getLogger(__name__)

async def handler(request: Request):
    LOG.info('Running a GET service info request')
    response_converted = build_beacon_service_info_response()
    return await json_stream(request, response_converted)
