"""
Dummy permissions server

We hard-code the dataset access in permission.json.

The token is a dummy token, built using the username.

"""
import logging
import os
from logging.config import dictConfig
from pathlib import Path
import yaml
import json

from aiohttp import web

LOG = logging.getLogger(__name__)

# Dummy permission database
with open('permissions.json', 'r') as stream:
    PERMISSIONS = json.load(stream)

async def permission(request):

    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        raise web.HTTPUnauthorized()

    access_token = auth[7:].strip() # 7 = len('Bearer ')
    # username = access_token.split('|')[0]
    username = access_token
    LOG.debug('username: %s', username)
    datasets = PERMISSIONS.get(username)
    if datasets is None:
        raise web.HTTPUnauthorized()

    if request.headers.get('Content-Type') == 'application/json':
        post_data = await request.json()
    else:
        post_data = await request.post() # request.json() crashes on empty data
        LOG.debug('POST DATA: %s', post_data)

    requested_datasets = post_data.get('datasets') # not a list
    LOG.debug('requested datasets: %s', requested_datasets)

    if requested_datasets:
        selected_datasets = set(requested_datasets.split(',')).intersection(datasets)
    else:
        selected_datasets = datasets
    LOG.debug('selected datasets: %s', selected_datasets)
    return web.json_response(list(selected_datasets or [])) # cuz python json doesn't like sets

    

def main(path=None):

    # Configure the logging
    log_file =  Path(__file__).parent / "logger.yml"
    if log_file.exists():
        with open(log_file, 'r') as stream:
            dictConfig(yaml.safe_load(stream))

    # Configure the beacon
    server = web.Application()

    # Configure the endpoints
    server.add_routes([web.post('/', permission)])

    web.run_app(server,
                host='0.0.0.0',
                port=5051,
                shutdown_timeout=0, ssl_context=None)


if __name__ == '__main__':
    main()


