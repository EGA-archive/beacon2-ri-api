import logging

from aiohttp import ClientSession, web

from ..conf import permissions_url
from ..utils.db import filter_out_non_public_datasets

LOG = logging.getLogger(__name__)

async def resolve_token(token, requested_datasets):
    # If the user is not authenticated (ie no token)
    # we pass (requested_datasets, False) to the database function: it will filter out the datasets list, with the public ones
    if token is None:
        public_datasets = [ name async for name in db.filter_out_non_public_datasets(requested_datasets)]
        return public_datasets, False

    # Otherwise, we have a token and resolve the datasets with the permissions server
    # The permissions server will:
    # * filter out the datasets list, with the ones the user has access to
    # * return _all_ the datasets the user has access to, in case the datasets list is empty
    async with ClientSession() as session:
        async with session.post(
                permissions_url,
                headers = { 'Authorization': 'Bearer ' + token,
                            'Accept': 'application/json'},
                json = { 'datasets': list(requested_datasets) }, # will set the Content-Type to application/json
        ) as resp:
            if resp.status > 200:
                LOG.error('Permissions server error %d', resp.status)
                error = await resp.text()
                LOG.error('Error: %s', error)
                raise web.HTTPUnauthorized(reason=error)
            
            authorized_datasets = await resp.json()
            return authorized_datasets, True
