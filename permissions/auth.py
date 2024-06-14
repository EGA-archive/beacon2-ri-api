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
import glob

from aiohttp import ClientSession, BasicAuth, FormData
from aiohttp import web
from beacon import conf
import os
from dotenv import load_dotenv

LOG = logging.getLogger(__name__)

def validate_access_token(access_token, idp_issuer, jwks_url, algorithm, aud):
    if not jwt.algorithms.has_crypto:
        print("No crypto support for JWT, please install the cryptography dependency")
        return False

    try:
        jwks_client = jwt.PyJWKClient(jwks_url, cache_jwk_set=True, lifespan=360)
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=[algorithm],
            issuer=idp_issuer,
            audience=aud,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
                "verify_aud": True,
                "verify_iss": True,
            },
        )
        LOG.error(data)
        return True
    except jwt.exceptions.PyJWTError as err:
        LOG.error(f"Error: {err}")
        return False

async def get_user_info(access_token):
    '''
    We use the access_token to get the user info.
    On failure (ie an invalid token), we try to get an explanation.
    '''
    LOG.debug('Token: %s', access_token)
    access_token_validation = False
    try:
        header = jwt.get_unverified_header(access_token)
        algorithm=header["alg"]
        decoded = jwt.decode(access_token, options={"verify_signature": False})
        issuer = decoded['iss']
        aud = decoded['aud']
        list_visa_datasets=[]
        visa_datasets=None
    except Exception:
        user = 'public'
        return user
    LOG.error(issuer)
    user_info=''
    idp_issuer=None
    for env_filename in glob.glob("/beacon/permissions/idp_providers/*.env"):
        load_dotenv(env_filename)
        IDP_ISSUER = os.getenv('ISSUER')
        LOG.error(IDP_ISSUER)
        if issuer == IDP_ISSUER:
            IDP_CLIENT_ID = os.getenv('CLIENT_ID')
            IDP_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
            IDP_USER_INFO = os.getenv('USER_INFO')
            IDP_INTROSPECTION = os.getenv('INTROSPECTION')
            IDP_JWKS_URL = os.getenv('JWKS_URL')
            idp_issuer = IDP_ISSUER
            user_info = IDP_USER_INFO
            idp_client_id = IDP_CLIENT_ID
            idp_client_secret = IDP_CLIENT_SECRET
            idp_introspection = IDP_INTROSPECTION
            idp_jwks_url = IDP_JWKS_URL
            break
        else:
            continue
    LOG.error(idp_issuer)
    
    if idp_issuer is None:
        raise web.HTTPUnauthorized('invalid token')
    
    access_token_validation = validate_access_token(access_token, idp_issuer, idp_jwks_url, algorithm, aud)
    if access_token_validation is False:
        raise web.HTTPUnauthorized('invalid token')
    
    LOG.error(user_info)
    user = None

    async with ClientSession() as session:
        async with session.post(idp_introspection,
                                auth=BasicAuth(idp_client_id, password=idp_client_secret),
                                data=FormData({ 'token': access_token, 'token_type_hint': 'access_token' }, charset='UTF-8')
        ) as resp:
            LOG.error('Response %s', resp.status)
            #LOG.debug('Response %s', resp)
            content = await resp.text()
            LOG.error('Content: %s', content)
            if resp.status == 200:
                pass
            else:
                LOG.error('Invalid token')
                user = 'public'
                return user, list_visa_datasets

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
                                if visa['iss']==idp_issuer:
                                    pass
                                else:
                                    raise web.HTTPUnauthorized('invalid visa token')
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
