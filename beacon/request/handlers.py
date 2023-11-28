import json
import asyncio
import logging
from aiohttp import ClientSession, web
from aiohttp.web_request import Request
from bson import json_util
from .. import conf
import yaml
import jwt

from beacon.request import ontologies
from beacon.request.model import Granularity, RequestParams
from beacon.response.build_response import (
    build_beacon_resultset_response,
    build_beacon_collection_response,
    build_beacon_boolean_response,
    build_beacon_count_response,
    build_filtering_terms_response,
    build_beacon_resultset_response_by_dataset
)
from beacon.utils.stream import json_stream
from beacon.db.datasets import get_datasets
from beacon.utils.auth import resolve_token

LOG = logging.getLogger(__name__)


def collection_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
        qparams = RequestParams(**json_body).from_request(request)
        entry_id = request.match_info["id"] if "id" in request.match_info else None
        # Get response
        entity_schema, count, records = db_fn(entry_id, qparams)
        response_converted = (
            [r for r in records] if records else []
        )
        response = build_beacon_collection_response(
            response_converted, count, qparams, lambda x, y: x, entity_schema
        )
        return await json_stream(request, response)

    return wrapper


def generic_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
        qparams = RequestParams(**json_body).from_request(request)
        skip = qparams.query.pagination.skip
        limit = qparams.query.pagination.limit
        LOG.debug(limit)
        LOG.debug(qparams)
        search_datasets = []
        authenticated=False
        access_token = request.headers.get('Authorization')


        
        LOG.debug(access_token)
        if access_token is not None:
            pass
        else:
            access_token = 'Bearer public'
        try:
            specific_datasets = qparams.query.request_parameters['datasets']
        except Exception:
            specific_datasets = []
        access_token = access_token[7:]  # cut out 7 characters: len('Bearer ')
        LOG.debug(access_token)

    

        authorized_datasets, authenticated, username = await resolve_token(access_token, search_datasets)

        LOG.debug(authorized_datasets)

        
        #LOG.debug('all datasets:  %s', all_datasets)
        LOG.info('resolved datasets:  %s', authorized_datasets)
        LOG.debug(authenticated)
        LOG.debug(specific_datasets)


        specific_datasets_unauthorized = []
        specific_datasets_unauthorized_and_found = []
        bio_list = []
        search_and_authorized_datasets = []
        specific_search_datasets = []
        # Get response
        if specific_datasets != []:
            for element in authorized_datasets:
                if element in specific_datasets:
                    search_and_authorized_datasets.append(element)
            for elemento in specific_datasets:
                if elemento not in search_and_authorized_datasets:
                    specific_datasets_unauthorized.append(elemento)
            qparams.query.request_parameters = {}
            qparams.query.request_parameters['datasets'] = '*******'
            _, _, datasets = get_datasets(None, qparams)
            beacon_datasets = [ r for r in datasets ]
            all_datasets = [r['id'] for r in beacon_datasets]
            
            response_datasets = [ r['id'] for r in beacon_datasets if r['id'] in search_and_authorized_datasets]
            LOG.debug(specific_search_datasets)
            LOG.debug(response_datasets)

            list_of_dataset_dicts=[]

            for data_r in response_datasets:
                dict_dataset = {}
                dict_dataset['dataset']=data_r
                dict_dataset['ids']=[ r['ids'] for r in beacon_datasets if r['id'] == data_r ]
                list_of_dataset_dicts.append(dict_dataset)

            for dataset_searched in specific_datasets_unauthorized:
                if dataset_searched not in all_datasets:
                    dict_dataset = {}
                    dict_dataset['dataset']=dataset_searched
                    dict_dataset['ids'] = ['Dataset not found']
                    LOG.debug(dict_dataset['dataset'])
                    LOG.debug(dict_dataset['ids'])
                    list_of_dataset_dicts.append(dict_dataset)
            
            for data_s in specific_datasets_unauthorized_and_found:
                dict_dataset = {}
                dict_dataset['dataset']=data_s
                dict_dataset['ids'] = ['Unauthorized dataset']
                list_of_dataset_dicts.append(dict_dataset)

            LOG.debug(specific_datasets_unauthorized_and_found)
            LOG.debug(specific_datasets_unauthorized)
            LOG.debug(list_of_dataset_dicts)

        else:
            qparams.query.request_parameters = {}
            qparams.query.request_parameters['datasets'] = '*******'
            _, _, datasets = get_datasets(None, qparams)
            beacon_datasets = [ r for r in datasets ]
            LOG.debug(authorized_datasets)
            specific_datasets = [ r['id'] for r in beacon_datasets if r['id'] not in authorized_datasets]
            response_datasets = [ r['id'] for r in beacon_datasets if r['id'] in authorized_datasets]
            LOG.debug(specific_datasets)
            LOG.debug(response_datasets)
            specific_datasets_unauthorized.append(specific_datasets)
            for unauth in specific_datasets_unauthorized:
                for unauth_spec in unauth:
                    biosample_ids = [ r['ids'] for r in beacon_datasets if r['id'] == unauth_spec ]
                    bio_list.append(biosample_ids)
            
            list_of_dataset_dicts=[]

            for data_r in response_datasets:
                dict_dataset = {}
                dict_dataset['dataset']=data_r
                dict_dataset['ids']=[ r['ids'] for r in beacon_datasets if r['id'] == data_r ]
                list_of_dataset_dicts.append(dict_dataset)
            
            for data_s in specific_datasets:
                dict_dataset = {}
                dict_dataset['dataset']=data_s
                dict_dataset['ids'] = ['Unauthorized dataset']
                list_of_dataset_dicts.append(dict_dataset)
            #LOG.debug(list_of_dataset_dicts)


            

        qparams = RequestParams(**json_body).from_request(request)

        if access_token != 'public':




            with open("/beacon/beacon/request/response_type.yml", 'r') as response_type_file:
                response_type_dict = yaml.safe_load(response_type_file)

            try:
                response_type = response_type_dict[username]
            except Exception:
                LOG.debug(Exception)
                response_type = ['boolean']
            if response_type is not None:
                for response_typed in response_type:    
                    LOG.debug(response_typed)        
                    if response_typed == 'boolean':
                        qparams.query.requested_granularity = Granularity.BOOLEAN
                    elif response_typed == 'count':
                        qparams.query.requested_granularity = Granularity.COUNT
                    elif response_typed == 'record':
                        qparams.query.requested_granularity = Granularity.RECORD
        

        entry_id = request.match_info.get('id', None)
        if entry_id == None:
            entry_id = request.match_info.get('variantInternalId', None)
        entity_schema, count, records = db_fn(entry_id, qparams)
        LOG.debug(entity_schema)

        if skip == 0 and limit !=0:
            start_record = 0
            finish_record = limit
        if limit == 0 and skip ==0:
            start_record = 0
            finish_record = count 
        if limit == 0 and skip !=0:
            start_record = skip
            finish_record = count 
        if skip !=0 and limit !=0:
            start_record = limit*skip
            finish_record = limit*skip + limit

        response_converted = records

        LOG.debug(qparams.query.requested_granularity)
        
        if qparams.query.requested_granularity == Granularity.BOOLEAN:
            response = build_beacon_boolean_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
        
        elif qparams.query.requested_granularity == Granularity.COUNT:
            if conf.max_beacon_granularity == Granularity.BOOLEAN:
                response = build_beacon_boolean_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
            else:
                response = build_beacon_count_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
        
        # qparams.query.requested_granularity == Granularity.RECORD:
        else:

            if conf.max_beacon_granularity == Granularity.BOOLEAN:
                response = build_beacon_boolean_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
            elif conf.max_beacon_granularity == Granularity.COUNT:
                response = build_beacon_count_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
            else:
                response = build_beacon_resultset_response_by_dataset(response_converted, list_of_dataset_dicts, count, qparams, lambda x, y: x, entity_schema, start_record, finish_record)
                
        return await json_stream(request, response)

    return wrapper

def filtering_terms_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
        qparams = RequestParams(**json_body).from_request(request)

        LOG.debug(qparams)
        
        search_datasets = []
        authenticated=False
        access_token = request.headers.get('Authorization')
        LOG.debug(access_token)
        if access_token is not None:
            try:
                specific_datasets = qparams.query.request_parameters['datasets']
            except Exception:
                specific_datasets = []
            access_token = access_token[7:]  # cut out 7 characters: len('Bearer ')

            
            authorized_datasets, authenticated = await resolve_token(access_token, search_datasets)
            LOG.debug(authorized_datasets)
            #LOG.debug('all datasets:  %s', all_datasets)
            LOG.info('resolved datasets:  %s', authorized_datasets)
            LOG.debug(authenticated)
            LOG.debug(specific_datasets)

            specific_datasets_unauthorized = []
            specific_datasets_unauthorized_and_found = []
            bio_list = []
            search_and_authorized_datasets = []
            specific_search_datasets = []
            # Get response
            if specific_datasets != []:
                for element in authorized_datasets:
                    if element in specific_datasets:
                        search_and_authorized_datasets.append(element)
                for elemento in specific_datasets:
                    if elemento not in search_and_authorized_datasets:
                        specific_datasets_unauthorized.append(elemento)
                qparams.query.request_parameters = {}
                qparams.query.request_parameters['datasets'] = '*******'
                _, _, datasets = get_datasets(None, qparams)
                beacon_datasets = [ r for r in datasets ]
                all_datasets = [r['id'] for r in beacon_datasets]
                
                response_datasets = [ r['id'] for r in beacon_datasets if r['id'] in search_and_authorized_datasets]
                LOG.debug(specific_search_datasets)
                LOG.debug(response_datasets)

                list_of_dataset_dicts=[]

                for data_r in response_datasets:
                    dict_dataset = {}
                    dict_dataset['dataset']=data_r
                    dict_dataset['ids']=[ r['ids'] for r in beacon_datasets if r['id'] == data_r ]
                    list_of_dataset_dicts.append(dict_dataset)

                for dataset_searched in specific_datasets_unauthorized:
                    if dataset_searched not in all_datasets:
                        dict_dataset = {}
                        dict_dataset['dataset']=dataset_searched
                        dict_dataset['ids'] = ['Dataset not found']
                        LOG.debug(dict_dataset['dataset'])
                        LOG.debug(dict_dataset['ids'])
                        list_of_dataset_dicts.append(dict_dataset)
                
                for data_s in specific_datasets_unauthorized_and_found:
                    dict_dataset = {}
                    dict_dataset['dataset']=data_s
                    dict_dataset['ids'] = ['Unauthorized dataset']
                    list_of_dataset_dicts.append(dict_dataset)

                LOG.debug(specific_datasets_unauthorized_and_found)
                LOG.debug(specific_datasets_unauthorized)

            else:
                qparams.query.request_parameters = {}
                qparams.query.request_parameters['datasets'] = '*******'
                _, _, datasets = get_datasets(None, qparams)
                beacon_datasets = [ r for r in datasets ]
                specific_datasets = [ r['id'] for r in beacon_datasets if r['id'] not in authorized_datasets]
                response_datasets = [ r['id'] for r in beacon_datasets if r['id'] in authorized_datasets]
                LOG.debug(specific_datasets)
                LOG.debug(response_datasets)
                specific_datasets_unauthorized.append(specific_datasets)
                for unauth in specific_datasets_unauthorized:
                    for unauth_spec in unauth:
                        biosample_ids = [ r['ids'] for r in beacon_datasets if r['id'] == unauth_spec ]
                        bio_list.append(biosample_ids)
                
                list_of_dataset_dicts=[]

                for data_r in response_datasets:
                    dict_dataset = {}
                    dict_dataset['dataset']=data_r
                    dict_dataset['ids']=[ r['ids'] for r in beacon_datasets if r['id'] == data_r ]
                    list_of_dataset_dicts.append(dict_dataset)
                
                for data_s in specific_datasets:
                    dict_dataset = {}
                    dict_dataset['dataset']=data_s
                    dict_dataset['ids'] = ['Unauthorized dataset']
                    list_of_dataset_dicts.append(dict_dataset)
                LOG.debug(list_of_dataset_dicts)
        else:
            list_of_dataset_dicts=[]

        qparams = RequestParams(**json_body).from_request(request)
        

        entry_id = request.match_info.get('id', None)
        entity_schema, count, records = db_fn(entry_id, qparams)

        response_converted = records
        
        if qparams.query.requested_granularity == Granularity.BOOLEAN:
            response = build_beacon_boolean_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
        
        elif qparams.query.requested_granularity == Granularity.COUNT:
            if conf.max_beacon_granularity == Granularity.BOOLEAN:
                response = build_beacon_boolean_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
            else:
                response = build_beacon_count_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
        
        # qparams.query.requested_granularity == Granularity.RECORD:
        else:

            if conf.max_beacon_granularity == Granularity.BOOLEAN:
                response = build_beacon_boolean_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
            elif conf.max_beacon_granularity == Granularity.COUNT:
                response = build_beacon_count_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
            else:
                response = build_filtering_terms_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
                
        return await json_stream(request, response)

    return wrapper
