import subprocess
import logging
import json
import aiohttp
from aiohttp import web
from aiohttp.web_request import Request
from beacon.db.datasets import get_datasets
from beacon.request import RequestParams
from beacon.response.build_response import build_beacon_error_response
from beacon.utils.auth import resolve_token
from beacon.utils.stream import json_stream
from bson import json_util

LOG = logging.getLogger(__name__)

async def handler(request: Request):
    LOG.error('Running an error request')

    LOG.error(request.url)

    # Fetch datasets info
    qparams = ''

    error = build_beacon_error_response(404, qparams, str('error'))

    
    raise web.HTTPNotFound(text=json.dumps(error), content_type='application/json')
