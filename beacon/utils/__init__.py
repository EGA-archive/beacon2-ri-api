import logging

from aiohttp import ClientSession, web

from ..conf import permissions_url
from ..utils.json import jsonb

LOG = logging.getLogger(__name__)

def filter_hstore(hstores, schema_name):
    for hstore in hstores:
        v = hstore.get(schema_name, None)
        if v is not None:
            yield jsonb(v)


async def resolve_token(token, requested_datasets):
    # If the user is not authenticated (ie no token)
    # we pass (requested_datasets, False) to the database function: it will filter out the datasets list, with the public ones
    if token is None:
        return requested_datasets, False

    # Otherwise, we have a token and resolve the datasets with the permissions server
    # The permissions server will:
    # * filter out the datasets list, with the ones the user has access to
    # * return _all_ the datasets the user has access to, in case the datasets list is empty
    async with ClientSession() as session:
        async with session.post(
                permissions_url,
                headers = { 'Authorization': 'Bearer ' + token,
                            'Accept': 'application/json'},
                json = { 'datasets': requested_datasets }, # will set the Content-Type to application/json
        ) as resp:
            if resp.status > 200:
                LOG.error('Permissions server error %d', resp.status)
                raise web.HTTPUnauthorized(reason=await resp.text())
            
            authorized_datasets = await resp.json()
            return authorized_datasets, True

