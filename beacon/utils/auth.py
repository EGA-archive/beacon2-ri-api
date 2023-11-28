import logging

from aiohttp import ClientSession, web

import asyncio

from beacon.db.datasets import filter_public_datasets
from ..conf import permissions_url, idp_user_info as idpu, lsaai_user_info as lsu

LOG = logging.getLogger(__name__)

async def resolve_token(token, requested_datasets_ids):
    # If the user is not authenticated (ie no token)
    # we pass (requested_datasets, False) to the database function: it will filter out the datasets list, with the public ones
    if token is None:
        public_datasets = [ d["name"] for d in filter_public_datasets(requested_datasets_ids) ]
        return public_datasets, False
    new_requested_datasets_ids=[]
    for dataset in requested_datasets_ids:
        dataset=str(dataset)
        new_requested_datasets_ids.append(dataset)
        requested_datasets_ids=new_requested_datasets_ids

    # Otherwise, we have a token and resolve the datasets with the permissions server
    # The permissions server will:
    # * filter out the datasets list, with the ones the user has access to
    # * return _all_ the datasets the user has access to, in case the datasets list is empty
    async with ClientSession() as session:
        async with session.post(
                permissions_url,
                headers={'Authorization': 'Bearer ' + token,
                         'Accept': 'application/json'},
                json={'datasets': requested_datasets_ids},  # will set the Content-Type to application/json
        ) as resp:
            '''
            if resp.status > 200:
                LOG.error('Permissions server error %d', resp.status)
                error = await resp.text()
                LOG.error('Error: %s', error)
                raise web.HTTPUnauthorized(body=error)
            '''
            content = await resp.content.read()
            content =  content.decode('utf-8')
            content_splitted= content.split(':')
            authorized_datasets = content_splitted[-1]
            authorized_datasets_list = authorized_datasets.split('"')
            try:
                username_ = content_splitted[1]
                username_list = username_.split('"')
                username = username_list[1]
            except Exception:
                username = ''
            LOG.debug(username)
            auth_datasets = []
            for auth_dataset in authorized_datasets_list:
                if ',' not in auth_dataset:
                    if '[' not in auth_dataset:
                        if ']' not in auth_dataset:
                            auth_datasets.append(auth_dataset)
            LOG.debug(auth_datasets)
            return auth_datasets, True, username
        
