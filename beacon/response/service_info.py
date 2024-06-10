import logging
from aiohttp.web_request import Request
from beacon.response.build_response import build_beacon_service_info_response, build_beacon_error_response
from beacon.utils.stream import json_stream
from aiohttp import web
import json

LOG = logging.getLogger(__name__)

async def handler(request: Request):
    try:
        LOG.info('Running a GET service info request')
        response_converted = build_beacon_service_info_response()
    except Exception as err:
        qparams = ''
        if str(err) == 'Not Found':
            error = build_beacon_error_response(404, qparams, str('error'))
            raise web.HTTPNotFound(text=json.dumps(error), content_type='application/json')
        elif str(err) == 'Bad Request':
            error = build_beacon_error_response(400, qparams, str('error'))
            raise web.HTTPBadRequest(text=json.dumps(error), content_type='application/json')
        elif str(err) == 'Bad Gateway':
            error = build_beacon_error_response(502, qparams, str('error'))
            raise web.HTTPBadGateway(text=json.dumps(error), content_type='application/json')
        elif str(err) == 'Method Not Allowed':
            error = build_beacon_error_response(405, qparams, str('error'))
            raise web.HTTPMethodNotAllowed(text=json.dumps(error), content_type='application/json')
        else:
            error = build_beacon_error_response(500, qparams, str('error'))
            raise web.HTTPInternalServerError(text=json.dumps(error), content_type='application/json')
    return await json_stream(request, response_converted)
