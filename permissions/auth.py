"""
Authentication / Token resolver

If the access token is a JWT token, and the verification key is loaded,
we could attempt to verify its signature, and avoid a round-trip to the IdP endpoint.
If not, we can't avoid the round-trip and that'll resolve whether the access token is 
valid.

For this implementation, we only implement contacting the userinfo endpoint.
No JWT signature verification.
"""
import json
import logging

from aiohttp import ClientSession, BasicAuth, FormData
from aiohttp import web



LOG = logging.getLogger(__name__)



idp_client_id     = 'beacon'
idp_client_secret = 'b26ca0f9-1137-4bee-b453-ee51eefbe7ba'
#idp_user_info = 'http://localhost:8080/oidc/userinfo'
#idp_user_info = 'http://ls-aai-mock:8080/oidc/userinfo'
idp_user_info  = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/userinfo'
#idp_introspection = 'http://ls-aai-mock:8080/oidc/introspect'
idp_introspection = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/token/introspect'
#idp_user_info     = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/userinfo'
#idp_introspection = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/token/introspect'







async def get_user_info(access_token):
    '''
    We use the access_token to get the user info.
    On failure (ie an invalid token), we try to get an explanation.
    '''
    LOG.debug('Token: %s', access_token)

    # Invalid access token
    
    async with ClientSession() as session:
        headers = { 'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token }
        payload = {'client_id': idp_client_id, 'client_secret': idp_client_secret, 'token': access_token }
        async with session.post(idp_introspection, headers=headers,
                                data=payload
        ) as resp:
            LOG.debug('Response %s', resp.status)
            #LOG.debug('Response %s', resp)
            if resp.status == 200:
                content = await resp.text()
                dict_content = json.loads(content)
                user = dict_content
            else:
                LOG.error('Content: %s', content)
                LOG.error('Invalid token')
                user = 'public'
                return user
            
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
                    user = 'public'
                    return user





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
        elif user == 'public':
            username = 'public'
        else:
            username = user.get('preferred_username')
        LOG.debug('username: %s', username)

        return await func(request, username)
    return decorated
