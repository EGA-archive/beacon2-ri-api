import logging

from aiohttp.http import SERVER_SOFTWARE
from aiohttp.web import StreamResponse

from .. import conf
from ..utils.json import json_iterencode

LOG = logging.getLogger(__name__)

_BUF_SIZE = getattr(conf, 'json_buffer_size', 1000)

# async def json_stream(request, data):
#     from aiohttp.web import json_response as aiohttp_json_response
#     return aiohttp_json_response(data)

async def json_stream(request, data):

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

    # LOG.debug('HTTP response stream for rows')
    buf = []
    for chunk in content_gen:
        if len(buf) < _BUF_SIZE:
            buf.append(chunk)
            continue
        # flush the buffer
        buf.append(chunk)
        chunk = ''.join(buf)
        buf = []
        await response.write(chunk.encode()) # utf-8
    if buf: # flush the remainder in the buffer
        chunk = ''.join(buf)
        await response.write(chunk.encode()) # utf-8

    # LOG.debug('HTTP response stream closing')
    await response.write_eof()
    return response
