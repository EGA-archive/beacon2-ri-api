import logging
from hashlib import sha256
import os

from django.contrib import messages

from . import conf
from .auth import do_logout
from .api import AuthAPIError, get_info

LOG = logging.getLogger(__name__)

# Context Processors

def info(request):
    try:
        user = request.session.get('user')
        LOG.debug('User: %s', user )
        user_id = user.get('sub') if user else None
        LOG.info('User id: %s', user_id )
        access_token = request.session.get('access_token')
        da_info = get_info(user_id, access_token = access_token)
    except AuthAPIError as ae:
        LOG.debug('Retrying without the token')
        do_logout(request)
        # retry without the token
        da_info = get_info(None)
        messages.warning(request, 'Session expired, you are logged out.')

    return {
        'BEACON': da_info,
        'ASSEMBLYIDS': conf.BEACON_ASSEMBLYIDS, # same for everyone
    }



def filters(request):
    return {
        'FILTERING_TERMS': conf.FILTERING_TERMS, # same for everyone
    }
    
