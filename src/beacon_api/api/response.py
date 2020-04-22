import json
from decimal import Decimal

from aiohttp.http import SERVER_SOFTWARE
from aiohttp.web import middleware, StreamResponse
from asyncpg import Record

from .. import conf

class BeaconEncoder(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, Decimal):
            return float(o)

        if isinstance(o, Record):
            return dict(record.items()) # temporarily

        # Let the base class default method raise the TypeError
        return super().default(o)


async def beacon_response(request, data):

    separators = (',',':') # (item_separator, key_separator) therefore, we make it compact
    content_gen = BeaconEncoder(separators=separators).iterencode(data)

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
