import logging
from hashlib import sha256

import requests
from django.core.cache import cache

from . import conf
from .auth import do_logout

LOG = logging.getLogger(__name__)

####################################

# Backend General Error
class BeaconAPIError(Exception):
    pass

# Backend answers with 401
class AuthAPIError(BeaconAPIError):
    pass

####################################

def make_cache_key(*args):
    #LOG.debug('Making Cache Key for: %s', args)
    m = sha256()
    for a in args:
        if a:
            m.update(str(a).encode())
    return m.hexdigest().lower()

def cached(func):
    def wrapper(*args, **kwargs): 
        cache_key = make_cache_key(*args) # ignoring kwargs
        cached_data = cache.get(cache_key)
        if cached_data:
            LOG.info('Rendering using cache | key: %s', cache_key)
            return cached_data
        else:
            data = func(*args, **kwargs)
            LOG.info('Caching results with key: %s', cache_key)
            cache.set(cache_key, data)
            return data
    return wrapper

@cached
def get_info(user, access_token = None):

    query_url = conf.CONF.get('beacon-api', 'info_url')
    if not query_url:
        raise BeaconAPIError('[beacon-api] info misconfigured')
    LOG.info('Beacon backend URL: %s', query_url)
    
    headers = { 'Accept': 'application/json',
                'Content-type': 'application/json',
    }
    if access_token: # we have a user
        LOG.debug('with a token')
        headers['Authorization'] = 'Bearer ' + access_token

    resp = requests.get(query_url, headers=headers)
    beacon_info = resp.json()

    if resp.status_code == 200:
        return beacon_info

    message = beacon_info.get('header',{}).get('userMessage', f'An error occured while contacting {query_url}')

    if resp.status_code == 401:
        # Auth error (like Invalid token)
        raise AuthAPIError(message)

    # In other cases
    raise Exception(f'Error {resp.status_code}: {message}')

# Using ckey as cache key
@cached
def get_filtering_terms(ckey):

    filtering_terms_url = conf.CONF.get('beacon-api', 'filtering_terms')
    if not filtering_terms_url:
        raise BeaconAPIError('[beacon-api] filtering_terms misconfigured')
    LOG.info('Beacon backend URL: %s', filtering_terms_url)
    
    # No access token
    headers = { 'Accept': 'application/json',
                'Content-type': 'application/json',
    }

    resp = requests.get(filtering_terms_url, headers=headers)
    data = resp.json()

    if resp.status_code == 200:
        return data.get('ontologyTerms')

    message = data.get('header',{}).get('userMessage', f'An error occured while contacting {filtering_terms_url}')
    raise Exception(f'Error {resp.status_code}: {message}')
