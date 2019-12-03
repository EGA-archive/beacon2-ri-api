import logging
import uuid
import base64
from urllib.parse import urlencode
import os

import requests
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib import messages

from .conf import CONF

LOG = logging.getLogger(__name__)

class BeaconLoginView(TemplateView):

    def get(self, request):

        next_url = request.GET.get('next', '/')
        LOG.debug('next URL: %s', next_url)

        access_token = request.session.get('access_token')
        if access_token:
            LOG.debug('Token: %s', access_token)
            return HttpResponseRedirect(next_url)

        redirect_uri = CONF.get('idp', 'redirect_uri')
        # redirect_uri += '?next=' if '?' not in redirect_uri else '&next='
        # redirect_uri += next_url
            
        code = request.GET.get('code')
        if code is None:
            LOG.debug('We must have a code')
            params = urlencode({ 'response_type': 'code',
                                 'client_id': CONF.get('idp', 'client_id'),
                                 'scope': CONF.get('idp', 'scope'),
                                 'state': uuid.uuid4(),
                                 'redirect_uri': redirect_uri })
            url = CONF.get('idp', 'authorize') + params
            LOG.debug('No code: Redirecting to URL: %s', url)
            return HttpResponseRedirect(url)

        state = request.GET.get('state')
        if not state:
            LOG.debug('We must have a state')
            raise HttpResponseBadRequest("Should have a state")

        headers = { 'Accept': 'application/json',
                    #'Content-type': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        }

        # We have a code and a state
        LOG.debug('Code: %s', code)

        basic = base64.b64encode('{}:{}'.format(CONF.get('idp', 'client_id'),
                                                CONF.get('idp', 'client_secret'))
                                 .encode())
        headers['Authorization'] = b'Basic '+basic

        params = { 'grant_type': 'authorization_code',
                   'code': code,
                   'redirect_uri': redirect_uri
        }
        LOG.debug( 'Post Request %r', params)
        res = requests.post(CONF.get('idp', 'access_token'),
                            headers=headers,
                            data=urlencode(params))
        if res.status_code > 200:
            LOG.error( 'Error when getting the access token: %r', res)
            return HttpResponseBadRequest('Invalid response for access token.')
        data = res.json()
        access_token = data.get('access_token')
        if not access_token: 
            LOG.error( 'Error when getting the access token: %r', res)
            return HttpResponseBadRequest('Failed to obtain OAuth access token.')

        LOG.debug('All good, we got an access token: %s...', access_token[:30])
        request.session['access_token'] = access_token
        id_token = data.get('id_token')
        if id_token:
            LOG.debug('And an ID token? %s...', id_token[:30])
            request.session['id_token'] = id_token

        # Fetch more info about the user
        res = requests.post(CONF.get('idp', 'user_info'),
                            headers=headers, 
                            data=urlencode({'access_token': access_token}))
        user = None
        if res.status_code == 200:
            user = res.json()

        LOG.info('The user is: %r', user)
        request.session['user'] = user
        # user_id = user.get('sub') if user else None
        # if user_id:
        #     messages.info(request, f'User {user_id} succesfully logged in')

        return HttpResponseRedirect(next_url)

class BeaconLogoutView(TemplateView):

    def get(self, request):
        do_logout(request)
        next_url = request.GET.get('next', '/')
        LOG.debug('next URL: %s', next_url)
        return HttpResponseRedirect(next_url)
        


def do_logout(request):
    LOG.info('Logging out: %s', request.session.get('user'))

    request.session['user']=None
    request.session['access_token']=None
    request.session['id_token']=None

    # None or del ?
    logout(request) # kills the session cookie

    #messages.info(request, f'Succesfully logged out')

    # Note: Not logging out from the IdP
