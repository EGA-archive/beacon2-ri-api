import logging
import os
import json
import uuid
import base64
from urllib.parse import urlencode

import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View
from django.conf import settings
from django.contrib.auth import logout

from . import conf
from . import forms

LOG = logging.getLogger(__name__)

####################################

def clean_empty_strings(iterable):
    for item in iterable:
        item = item.strip()
        if item:
            yield item

####################################

class BaseView(TemplateView):

    def get(self, request):

        form = getattr(forms, self.formbase)()

        ctx = { 'form': form,
                'selected_datasets': set(),
                'filters': set(),
                'beacon_response': None,
        }
        return render(request, 'index.html', ctx)

    def post(self, request):

        form = getattr(forms, self.formbase)(request.POST)

        selected_datasets = set(request.POST.getlist("datasetIds", []))
        LOG.debug('selected_datasets: %s', selected_datasets )
        filters = set( clean_empty_strings( request.POST.getlist("filters", []) ) )
        LOG.debug('filters: %s', filters )

        ctx = { 'form': form,
                'selected_datasets': selected_datasets,
                'filters': filters,
        }

        # Form validation... for the regex
        if not form.is_valid():
            return render(request, 'index.html', ctx)

        # Valid Form 
        params_d = form.query_deconstructed_data
        LOG.debug('Deconstructed Data: %s', params_d)

        #params_d['datasets'] = ','.join(selected_datasets) if selected_datasets else 'all'
        if selected_datasets:
            params_d['datasetIds'] = ','.join(selected_datasets) 
        if filters:
            params_d['filters'] = ','.join(filters)

        # Don't check anything and forward to backend        
        query_url = self.api_endpoint
        if not query_url:
            return render(request, 'error.html', { 'message': self.api_endpoint_error })
 
        query_url += urlencode(params_d, safe=',')
        LOG.debug('Forwarding to %s',query_url)

        # Access token
        headers = {}
        access_token = request.session.get('access_token')
        if access_token:
            LOG.debug('with a token: %s', access_token)
            headers['Authorization'] = 'Bearer ' + access_token
        else:
            LOG.debug('No Access token supplied')
        
        # Forwarding the request to the Beacon API
        r = requests.get(query_url,headers=headers)
        LOG.debug('------------------- %s', r)
        if not r:
            return render(request, 'error.html', {'message':'Beacon backend API not available' })

        response = None
        if r.status_code == 200:
            response = r.json()

        #LOG.debug('Response: %s', response)

        ctx['beacon_response'] = response
        ctx['query_url'] = query_url
        ctx['beacon_query'] = { 'params': params_d, 
                                'exists': 'Y' if response.get('exists', False) else 'N'
        }

        return render(request, 'index.html', ctx)



class BeaconQueryView(BaseView):
    formbase = 'QueryForm'
    api_endpoint = conf.CONF.get('beacon-api', 'query')
    api_endpoint_error = '[beacon-api] query endpoint misconfigured'
    # cheat_data = {
    #     'query': "1 : 13272 G > C",
    #     'assemblyId': 'grch37',
    #     'includeDatasetResponses': 'ALL',
    #     #'filters': ['ICD-10:XVI'],
    #     'filters': ['PATO:0000383', 'HP:0011007>=49', 'EFO:0009656'],
    # }

class BeaconSNPView(BaseView):
    formbase = 'QueryForm'
    api_endpoint = conf.CONF.get('beacon-api', 'genomic_snp')
    api_endpoint_error = '[beacon-api] genomic_snp endpoint misconfigured'
    # cheat_data = {
    #     'query': "1 : 13272 G > C",
    #     'assemblyId': 'GRCh37',
    #     'includeDatasetResponses': 'HIT',
    #     'filters': ['csvs.tech:1','csvs.tech:3'],
    # }

class BeaconRegionView(BaseView):
    formbase = 'QueryRegionForm'
    api_endpoint = conf.CONF.get('beacon-api', 'genomic_region')
    api_endpoint_error = '[beacon-api] genomic_region endpoint misconfigured'
    # cheat_data = {
    #     'query': "1 : 14900 - 15000",
    #     'assemblyId': 'grch37',
    #     'includeDatasetResponses': 'ALL',
    # }


class BeaconAccessLevelsView(TemplateView):

    def get(self, request):

        query_url = conf.CONF.get('beacon-api', 'access_levels', fallback=None)
        if not query_url:
            return render(request, 'error.html', {'message':'[beacon-api] access_levels is misconfigured' })

        if request.GET:
            query_url += '?' + request.GET.urlencode()

        LOG.info('Contacting Beacon backend: %s', query_url)
        headers = { 'Accept': 'application/json',
                    'Content-type': 'application/json',
        }

        access_token = request.session.get('access_token')
        if access_token:
            headers['Authorization'] = 'Bearer ' + access_token
        else:
            LOG.debug('No Access token supplied')

        resp = requests.get(query_url, headers=headers)
        if resp.status_code > 200:
            return render(request, 'error.html', {'message':'Backend not available' })

        ctx = resp.json()

        ctx['fieldsParam'] = True if request.GET.get('includeFieldDetails', 'false') == 'true' else False
        ctx['datasetsParam'] = True if request.GET.get('displayDatasetDifferences', 'false') == 'true' else False

        return render(request, 'access_levels.html', ctx)


def get_filters(word):
    count = 0
    for k,v in conf.FILTERING_TERMS.items():
        if not word or word.lower() in v.lower():
            count+=1
            
            if count > settings.AUTOCOMPLETE_LIMIT: # last word in the list
                yield (settings.AUTOCOMPLETE_ELLIPSIS, settings.AUTOCOMPLETE_ELLIPSIS)
                break
            
            yield (k,v)


class BeaconFilteringTermsView(View):
    
    def get(self,request, term=''): # empty string for all words
        #print(f'chosen word: "{term}"')
        if term is None:
            return JsonResponse( [], safe=False)

        terms = [ {'value': k, 'label': v }
                  for k,v in get_filters(term) ]

        return JsonResponse( terms, safe=False)

class TestingView(View):
    def get(self, request):
        template_name = 'testing.html'
        ctx = {}
        return render(request, template_name, ctx)


class BeaconSamplesView(BaseView):
    formbase = 'QuerySamplesForm'
    api_endpoint = conf.CONF.get('beacon-api', 'samples')
    api_endpoint_error = '[beacon-api] samples endpoint misconfigured'
    # cheat_data = {
    #     'query': "1 : 14900 - 15000",
    #     'assemblyId': 'grch37',
    #     'includeDatasetResponses': 'ALL',
    # }