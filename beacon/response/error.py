import subprocess
import logging
import json
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

    # Fetch datasets info
    qparams = ''
    
    response_converted= build_beacon_error_response(404, qparams, 'Not Found')
    return await json_stream(request, response_converted)
