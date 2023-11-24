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
import jwt

from aiohttp import ClientSession, BasicAuth, FormData
from aiohttp import web
from beacon import conf


LOG = logging.getLogger(__name__)


idp_user_info = conf.idp_user_info
lsaai_user_info = conf.lsaai_user_info

#idp_user_info = 'http://localhost:8080/oidc/userinfo'
#idp_user_info = 'http://ls-aai-mock:8080/oidc/userinfo'
#idp_user_info  = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/userinfo'
#idp_introspection = 'http://ls-aai-mock:8080/oidc/introspect'
#idp_introspection = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/token/introspect'
#idp_user_info     = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/userinfo'
#idp_introspection = 'http://idp:8080/auth/realms/Beacon/protocol/openid-connect/token/introspect'

async def get_user_info(access_token):
    '''
    We use the access_token to get the user info.
    On failure (ie an invalid token), we try to get an explanation.
    '''
    LOG.debug('Token: %s', access_token)

    # Invalid access token
    '''
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
                #LOG.error('Content: %s', content)
                LOG.error('Invalid token')
                user = 'public'
                return user
        '''
    decoded = jwt.decode(access_token, options={"verify_signature": False})
    LOG.error(decoded)
    issuer = decoded['iss']
    list_visa_datasets=[]
    visa_datasets=None

    if issuer in conf.trusted_issuers:
        pass
    else:
        raise web.HTTPUnauthorized('invalid token')
            
    user = None
    async with ClientSession(trust_env=True) as session:
        headers = { 'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token }
        LOG.debug('Contacting %s', idp_user_info)
        async with session.get(idp_user_info, headers=headers) as resp:
            LOG.debug('Response %s', resp)
            if resp.status == 200:
                user = await resp.json()
                LOG.error(user)
                return user, list_visa_datasets
            else:
                content = await resp.text()
                LOG.error('Not a Keycloak token')
                #LOG.error('Content: %s', content)
                user = 'public'
                
    if user == 'public':
        async with ClientSession(trust_env=True) as session:
            headers = { 'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token }
            LOG.debug('Contacting %s', lsaai_user_info)
            async with session.get(lsaai_user_info, headers=headers) as resp:
                LOG.debug('Response %s', resp)
                if resp.status == 200:
                    user = await resp.json()
                    try:
                        visa_datasets = user['ga4gh_passport_v1']
                    except Exception:
                        pass
                    if visa_datasets is not None:
                        for visa_dataset in visa_datasets:
                            try:
                                visa = jwt.decode(visa_dataset, options={"verify_signature": False}, algorithms=["RS256"])
                                dataset_url = visa["ga4gh_visa_v1"]["value"]
                                dataset_url_splitted = dataset_url.split('/')
                                visa_dataset = dataset_url_splitted[-1]
                                list_visa_datasets.append(visa_dataset)
                            except Exception:
                                visa_dataset = None
                    LOG.error('list_visa: {}'.format(list_visa_datasets))
                    return user, list_visa_datasets
                else:
                    content = await resp.text()
                    LOG.error('Not a LS AAI token')
                    LOG.error('Content: %s', content)
                    user = 'public'
                    return user, list_visa_datasets


def bearer_required(func):

    async def decorated(request):
        
        auth = request.headers.get('Authorization')
        if not auth or not auth.lower().startswith('bearer '):
            raise web.HTTPUnauthorized()

        access_token = auth[7:].strip() # 7 = len('Bearer ')

        # We make a round-trip to the userinfo. We might not have a JWT token.
        user, list_visa_datasets = await get_user_info(access_token)
        LOG.info('The user is: %r', user)
        if user is None:
            raise web.HTTPUnauthorized()
        elif user == 'public':
            username = 'public'
        else:
            username = user.get('preferred_username')
        LOG.debug('username: %s', username)

        return await func(request, username, list_visa_datasets)
    return decorated
