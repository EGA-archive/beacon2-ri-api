"""
Authentication / Token resolver

If the access token is a JWT token, and the verification key is loaded,
we could attempt to verify its signature, and avoid a round-trip to the IdP endpoint.
If not, we can't avoid the round-trip and that'll resolve whether the access token is 
valid.

For this implementation, we only implement contacting the userinfo endpoint.
No JWT signature verification.
"""

import logging

from aiohttp import ClientSession, BasicAuth, FormData
from aiohttp import web



LOG = logging.getLogger(__name__)



idp_client_id     = 'permissions'
idp_client_secret = 'c0285717-1bfb-4b32-b01d-d663470ce7c4'
#idp_user_info = 'http://localhost:8080/oidc/userinfo'
idp_user_info = 'http://ls-aai-mock:8080/oidc/userinfo'
#idp_user_info  = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/userinfo'
idp_introspection = 'http://ls-aai-mock:8080/oidc/introspect'
#idp_introspection = 'http://idp:8000/auth/realms/Beacon/protocol/openid-connect/token/introspect'
#idp_user_info     = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/userinfo'
#idp_introspection = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/token/introspect'







async def get_user_info(access_token):
    '''
    We use the access_token to get the user info.
    On failure (ie an invalid token), we try to get an explanation.
    '''
    LOG.debug('Token: %s', access_token)

    user = None
    async with ClientSession(trust_env=True) as session:
        headers = { 'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token }
        LOG.debug('Contacting %s', idp_user_info)
        async with session.get(idp_user_info, headers=headers) as resp:
            LOG.debug('Response %s', resp)
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



def bearer_required(func):

    async def decorated(request):
        
        auth = request.headers.get('Authorization')
        if not auth or not auth.lower().startswith('bearer '):
            raise web.HTTPUnauthorized()

        access_token = auth[7:].strip() # 7 = len('Bearer ')

        # We make a round-trip to the userinfo. We might not have a JWT token.
        user = await get_user_info(access_token)
        LOG.info('The user is: %r', user)
        if user is None:
            raise web.HTTPUnauthorized()
        username = user.get('preferred_username')
        LOG.debug('username: %s', username)

        return await func(request, username)
    return decorated
