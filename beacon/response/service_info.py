import logging
from aiohttp.web_request import Request
from beacon.response.build_response import build_beacon_service_info_response, build_beacon_error_response
from beacon.utils.stream import json_stream

LOG = logging.getLogger(__name__)

async def handler(request: Request):
    try:
        LOG.info('Running a GET service info request')
        response_converted = build_beacon_service_info_response()
    except Exception as err:
        qparams = ''
        if str(err) == 'Not Found':
            response_converted = build_beacon_error_response(404, qparams, str(err))
        else:
            response_converted = build_beacon_error_response(500, qparams, str(err))
    return await json_stream(request, response_converted)
