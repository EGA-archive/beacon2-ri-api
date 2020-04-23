import logging

from aiohttp.http import SERVER_SOFTWARE
from aiohttp.web import middleware, StreamResponse

from .. import conf
from ..utils.json import json_iterencode

LOG = logging.getLogger(__name__)

async def beacon_response(request, data):

    # Running this first, in case it raises an error
    # so we don't start the StreamResponse yet
    content_gen = [chunk async for chunk in json_iterencode(data)]
    
    LOG.debug('HTTP response stream')
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Server': f'{conf.beacon_name} {conf.version} (based on {SERVER_SOFTWARE})'
    }
    response = StreamResponse(headers=headers)

    # response.enable_chunked_encoding()
    await response.prepare(request)

    for chunk in content_gen:
        # print(chunk)
        await response.write(chunk.encode()) # utf-8

    await response.write_eof()
    return response


# For later, in case all the endpoints do the same thing,
# then we put it in the middleware.
@middleware
async def middleware(request, handler):
    data = await handler(request)
    return await beacon_response(request, data)
