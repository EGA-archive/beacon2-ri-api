import logging

from ..api.response import beacon_response
from ..api.db import fetch_viral
from ..api.exceptions import BeaconBadRequest
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import (RegexField,
                                 ChoiceField,
                                 IntegerField,
                                 ListField)

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class Parameters(RequestParameters):
    offset = IntegerField(min_value=0, default=0)
    limit = IntegerField(min_value=0, default=10)

# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

proxy = Parameters()

async def handler(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given QUERY.
    It uses the '/query' path and expects some parameters.
    """
    LOG.info('Running a query request')
    qparams_raw, qparams_db = await proxy.fetch(request)
    LOG.debug("Original Query Parameters: %s", qparams_raw)

    # print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy, LOG)

    # Fetch info from the database. It returns an async gen
    # beacon_response knows how to loop through it
    response = fetch_viral(qparams_db)

    return await beacon_response(request, response)

from aiohttp.web import StreamResponse
from .. import conf
async def handler_html(request):
    qparams_raw, qparams_db = await proxy.fetch(request)
    # print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy, LOG)

    # Fetch info from the database. It returns an async gen
    # beacon_response knows how to loop through it
    rows = fetch_viral(qparams_db)

    LOG.debug('----- HTTP response stream')
    headers = {
        'Content-Type': 'text/html;charset=utf-8',
        'Server': f'{conf.beacon_name} {conf.version}'
    }
    response = StreamResponse(headers=headers)

    # response.enable_chunked_encoding()
    await response.prepare(request)

    keys = [ "id",
             "dataset_id",
             "chromosome",
             "variant_id ",
             "reference",
             "alternate",
             " start ",
             "end",
             "type",
             "sv_length",
             "variant_cnt",
             "call_cnt",
             "sample_cnt",
             "matching_sample_cnt",
             " frequency"]

    await response.write(f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{conf.beacon_name} {conf.version}</title>

  <style>
    body {{ color: #212529; }}
    table {{ border-collapse: collapse; width: 100%; }}
    thead {{ color: #212529; }}
    th {{ background-color: #6c7ae0; color: #fff; font-size: 18px; line-height: 1.4; padding: 1em 0.5em; }}
    tbody tr:nth-child(2n) {{ background-color: #f8f6ff; }}
  </style>
</head>
<body>
  <table>
   <thead><tr>
'''.encode()) # utf-8
    for key in keys:
        await response.write(b'<th>')
        await response.write(key.encode())
        await response.write(b'</th>')
    await response.write(b'</tr></thead><tbody>') # utf-8
    LOG.debug('----- output for rows')
    async for row in rows:
        await response.write(b'<tr>')
        for key in keys:
            val = row.get(key)
            if val is None:
                val = '-'
            col = '<td>{}</td>'.format(val)
            await response.write(col.encode()) # utf-8
        await response.write(b'</tr>')
    LOG.debug('----- done with the rows')
    await response.write(b'</tr></tbody></table></body></html>')
    await response.write_eof()

    LOG.debug('----- HTTP response stream done')
    return response
