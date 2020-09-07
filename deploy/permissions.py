"""
Dummy permissions server

We hard-code the dataset permissions.

"""
import logging
import os
from logging.config import dictConfig
from pathlib import Path


import yaml
from aiohttp import web
from aiohttp import ClientSession, BasicAuth, FormData

LOG = logging.getLogger(__name__)

# Dummy permission database
PERMISSIONS = {
    "john": ["GiaB", "dataset-registered", "dataset-controlled"],
    "jane": ["GiaB", "dataset-registered"],
}


idp_client_id     = 'permissions'
idp_client_secret = 'c0285717-1bfb-4b32-b01d-d663470ce7c4'
idp_user_info     = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/userinfo'
idp_introspection = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/token/introspect'


async def get_user_info(access_token):
    '''
    We use the access_token to get the user info.
    On failure (ie an invalid token), we try to get an explanation.
    '''
    LOG.debug('Token: %s', access_token)

    user = None
    async with ClientSession() as session:
        headers = { 'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token }
        LOG.debug('Contacting %s', idp_user_info)
        async with session.get(idp_user_info, headers=headers) as resp:
            # LOG.debug('Response %s', resp)
            if resp.status == 200:
                user = await resp.json()
                return user
            else:
                content = await resp.text()
                LOG.error('Content: %s', content)

    # Invalid access token
    LOG.error('Invalid token')
    async with ClientSession() as session:
        async with session.post(idp_introspection,
                                auth=BasicAuth(idp_client_id, password=idp_client_secret),
                                data=FormData({ 'token': access_token, 'token_type_hint': 'access_token' }, charset='UTF-8')
        ) as resp:
            LOG.debug('Response %s', resp.status)
            #LOG.debug('Response %s', resp)
            content = await resp.text()
            LOG.debug('Content: %s', content)
    raise web.HTTPUnauthorized()

async def permission(request):

    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        raise web.HTTPUnauthorized()

    access_token = auth[7:].strip() # 7 = len('Bearer ')

    user = await get_user_info(access_token)
    LOG.info('The user is: %r', user)
    if user is None:
        raise web.HTTPUnauthorized()

    username = user.get('preferred_username')
    LOG.debug('username: %s', username)

    if request.headers.get('Content-Type') == 'application/json':
        post_data = await request.json()
        requested_datasets = post_data.get('datasets') # already a list
    else:
        post_data = await request.post() # request.json() crashes on empty data
        LOG.debug('POST DATA: %s', post_data)
        requested_datasets = post_data.get('datasets').split(',')

    LOG.debug('requested datasets: %s', requested_datasets)

    datasets = PERMISSIONS.get(username)
    if requested_datasets:
        selected_datasets = set(requested_datasets).intersection(datasets)
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


