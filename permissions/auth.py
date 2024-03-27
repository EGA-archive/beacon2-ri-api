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
import os
from dotenv import load_dotenv

load_dotenv()

LSAAI_CLIENT_ID = os.getenv('LSAAI_CLIENT_ID')
KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID')


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

    try:
        decoded = jwt.decode(access_token, options={"verify_signature": False})
        LOG.error(decoded)
        issuer = decoded['iss']
        audience = decoded['aud']
        list_visa_datasets=[]
        visa_datasets=None
    except Exception:
        user = 'public'
        return user
    LOG.error(issuer)
    user_info=''
    if issuer == conf.lsaai_issuer and audience == LSAAI_CLIENT_ID:
        user_info = lsaai_user_info
    elif issuer == conf.idp_issuer and audience == KEYCLOAK_CLIENT_ID:
        user_info = idp_user_info
    else:
        raise web.HTTPUnauthorized('invalid token')
    
    LOG.error(user_info)
    user = None
                
    async with ClientSession(trust_env=True) as session:
        headers = { 'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token }
        LOG.error('Contacting %s', user_info)
        async with session.get(user_info, headers=headers) as resp:
            LOG.error('Response %s', resp)
            if resp.status == 200:
                user = await resp.json()
                try:
                    visa_datasets = user['ga4gh_passport_v1']
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
                except Exception:
                    pass
                LOG.error('list_visa: {}'.format(list_visa_datasets))
                return user, list_visa_datasets
            else:
                content = await resp.text()
                LOG.error('Invalid token')
                LOG.error('Content: %s', content)
                user = 'public'
                return user, list_visa_datasets


def bearer_required(func):

    async def decorated(request):
        
        auth = request.headers.get('Authorization')
        if not auth or not auth.lower().startswith('bearer '):
            raise web.HTTPUnauthorized()
        list_visa_datasets=[]
        access_token = auth[7:].strip() # 7 = len('Bearer ')
        LOG.error(access_token)
        # We make a round-trip to the userinfo. We might not have a JWT token.
        try:
            user, list_visa_datasets = await get_user_info(access_token)
        except Exception:
            user = 'public'
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
