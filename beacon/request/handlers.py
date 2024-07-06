import json
import asyncio
import logging
from aiohttp import ClientSession, web
from aiohttp.web_request import Request
from bson import json_util
from .. import conf
import yaml
import jwt
import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from beacon.request import ontologies
from beacon.request.model import Granularity, RequestParams
from beacon.response.build_response import (
    build_beacon_resultset_response,
    build_beacon_collection_response,
    build_beacon_boolean_response,
    build_beacon_count_response,
    build_filtering_terms_response,
    build_beacon_resultset_response_by_dataset,
    build_beacon_error_response
)
from beacon.utils.stream import json_stream
from beacon.db.datasets import get_datasets
from beacon.utils.auth import resolve_token
from beacon.db.schemas import DefaultSchemas

LOG = logging.getLogger(__name__)


def collection_handler(db_fn, request=None):
    async def wrapper(request: Request):
        try:
            # Get params
            json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
            qparams = RequestParams(**json_body).from_request(request)
            entry_id = request.match_info["id"] if "id" in request.match_info else None
            LOG.debug(entry_id)
            # Get response
            entity_schema, count, records = db_fn(entry_id, qparams)
            if qparams.query.test_mode:
                if entity_schema==DefaultSchemas.COHORTS:
                    with open("/beacon/beacon/response/testMode/cohorts.json", 'r') as json_file:
                        data = json.load(json_file)
                    response_converted=data
                    count=1
                    entity_schema=DefaultSchemas.COHORTS
                elif entity_schema==DefaultSchemas.DATASETS:
                    with open("/beacon/beacon/response/testMode/datasets.json", 'r') as json_file:
                        data = json.load(json_file)
                    response_converted=data
                    count=1
                    entity_schema=DefaultSchemas.DATASETS
                response = build_beacon_collection_response(
                    response_converted, count, qparams, lambda x, y: x, entity_schema
                )
            else:
                response_converted = (
                    [r for r in records] if records else []
                )
                LOG.debug(entity_schema)
                response = build_beacon_collection_response(
                    response_converted, count, qparams, lambda x, y: x, entity_schema
                )
        except Exception as err:
            qparams = ''
            if str(err) == 'Not Found':
                error = build_beacon_error_response(404, qparams, str(err))
                raise web.HTTPNotFound(text=json.dumps(error), content_type='application/json')
            elif str(err) == 'Bad Request':
                error = build_beacon_error_response(400, qparams, str(err))
                raise web.HTTPBadRequest(text=json.dumps(error), content_type='application/json')
            elif str(err) == 'Bad Gateway':
                error = build_beacon_error_response(502, qparams, str(err))
                raise web.HTTPBadGateway(text=json.dumps(error), content_type='application/json')
            elif str(err) == 'Method Not Allowed':
                error = build_beacon_error_response(405, qparams, str(err))
                raise web.HTTPMethodNotAllowed(text=json.dumps(error), content_type='application/json')
            else:
                LOG.debug(err)
                error = build_beacon_error_response(500, qparams, str(err))
                raise web.HTTPInternalServerError(text=json.dumps(error), content_type='application/json')
        return await json_stream(request, response)

    return wrapper

def generic_handler(db_fn, request=None):
    async def wrapper(request: Request):
        try:
            # Get params
            json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
            qparams = RequestParams(**json_body).from_request(request)
            if qparams.query.test_mode:
                LOG.debug('entering the test Mode')
                if 'individuals' in str(db_fn):
                    with open("/beacon/beacon/response/testMode/individuals.json", 'r') as json_file:
                        response_converted = json.load(json_file)
                    entity_schema=DefaultSchemas.INDIVIDUALS
                elif 'analyses' in str(db_fn):
                    with open("/beacon/beacon/response/testMode/analyses.json", 'r') as json_file:
                        response_converted = json.load(json_file)
                    entity_schema=DefaultSchemas.ANALYSES
                elif 'biosamples' in str(db_fn):
                    with open("/beacon/beacon/response/testMode/biosamples.json", 'r') as json_file:
                        response_converted = json.load(json_file)
                    entity_schema=DefaultSchemas.BIOSAMPLES
                elif 'variants' in str(db_fn):
                    with open("/beacon/beacon/response/testMode/genomicVariations.json", 'r') as json_file:
                        response_converted = json.load(json_file)
                    entity_schema=DefaultSchemas.GENOMICVARIATIONS
                elif 'runs' in str(db_fn):
                    with open("/beacon/beacon/response/testMode/runs.json", 'r') as json_file:
                        response_converted = json.load(json_file)
                    entity_schema=DefaultSchemas.RUNS
                datasets_docs={}
                datasets_docs['testModeDataset']=response_converted
                datasets_count={}
                datasets_count['testModeDataset']=1
                count=1
                response = build_beacon_resultset_response_by_dataset(datasets_docs, datasets_count, count, qparams, lambda x, y: x, entity_schema)
            else:
                skip = qparams.query.pagination.skip
                limit = qparams.query.pagination.limit
                #LOG.debug(limit)
                LOG.debug(qparams)
                search_datasets = []
                authenticated=False
                access_token = request.headers.get('Authorization')
                
                #LOG.debug(access_token)
                if access_token is not None:
                    pass
                else:
                    access_token = 'Bearer public'
                try:
                    specific_datasets = qparams.query.request_parameters['datasets']
                except Exception:
                    specific_datasets = []
                access_token = access_token[7:]  # cut out 7 characters: len('Bearer ')
                #LOG.debug(access_token)

            

                authorized_datasets, authenticated, username = await resolve_token(access_token, search_datasets)

                #LOG.debug(authorized_datasets)
                #LOG.debug(username)
                
                ##LOG.debug('all datasets:  %s', all_datasets)
                LOG.info('resolved datasets:  %s', authorized_datasets)
                #LOG.debug(authenticated)
                #LOG.debug(specific_datasets)


                specific_datasets_unauthorized = []
                search_and_authorized_datasets = []
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

                else:
                    qparams.query.request_parameters = {}
                    qparams.query.request_parameters['datasets'] = '*******'
                    _, _, datasets = get_datasets(None, qparams)
                    beacon_datasets = [ r for r in datasets ]
                    #LOG.debug(authorized_datasets)
                    specific_datasets = [ r['id'] for r in beacon_datasets if r['id'] not in authorized_datasets]
                    response_datasets = [ r['id'] for r in beacon_datasets if r['id'] in authorized_datasets]
                    #LOG.debug(specific_datasets)
                    #LOG.debug(response_datasets)
                    specific_datasets_unauthorized.append(specific_datasets)


                qparams = RequestParams(**json_body).from_request(request)
                include = qparams.query.include_resultset_responses


                if access_token != 'public':


                    with open("/beacon/beacon/request/response_type.yml", 'r') as response_type_file:
                        response_type_dict = yaml.safe_load(response_type_file)
                    #LOG.debug(response_type_dict)
                    try:
                        response_type = response_type_dict[username]
                    except Exception:
                        pass
                    try:
                        if response_type is not None:
                            for response_typed in response_type:    
                                #LOG.debug(response_typed)        
                                if response_typed == 'boolean':
                                    qparams.query.requested_granularity = Granularity.BOOLEAN
                                elif response_typed == 'count':
                                    qparams.query.requested_granularity = Granularity.COUNT
                                elif response_typed == 'record':
                                    qparams.query.requested_granularity = Granularity.RECORD
                    except Exception:
                        pass
                

                entry_id = request.match_info.get('id', None)
                if entry_id == None:
                    entry_id = request.match_info.get('variantInternalId', None)
                datasets_docs={}
                datasets_count={}
                #LOG.debug(response_datasets)
                new_count=0
                loop = asyncio.get_running_loop()
                with ThreadPoolExecutor() as pool:
                    done, pending = await asyncio.wait(fs=[loop.run_in_executor(pool, db_fn, entry_id, qparams, dataset) for dataset in response_datasets],
                    return_when=asyncio.ALL_COMPLETED
                    )
                for task in done:
                    entity_schema, count, dataset_count, records, dataset = task.result()
                    if dataset_count != -1:
                        new_count+=dataset_count
                        datasets_docs[dataset]=records
                        datasets_count[dataset]=dataset_count
                
                if include != 'NONE':
                    count=new_count
                else:
                    if limit == 0 or new_count < limit:
                        pass
                    else:
                        count = limit
                
                #LOG.debug(count)
                response_converted = records


                #LOG.debug(qparams.query.requested_granularity)
                
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
                    elif include == 'NONE':
                        response = build_beacon_resultset_response(response_converted, count, qparams, lambda x, y: x, entity_schema)
                    else:
                        response = build_beacon_resultset_response_by_dataset(datasets_docs, datasets_count, count, qparams, lambda x, y: x, entity_schema)
        except Exception as err:
            qparams = ''
            if str(err) == 'Not Found':
                error = build_beacon_error_response(404, qparams, str(err))
                raise web.HTTPNotFound(text=json.dumps(error), content_type='application/json')
            elif str(err) == 'Bad Request':
                error = build_beacon_error_response(400, qparams, str(err))
                raise web.HTTPBadRequest(text=json.dumps(error), content_type='application/json')
            elif str(err) == 'Bad Gateway':
                error = build_beacon_error_response(502, qparams, str(err))
                raise web.HTTPBadGateway(text=json.dumps(error), content_type='application/json')
            elif str(err) == 'Method Not Allowed':
                error = build_beacon_error_response(405, qparams, str(err))
                raise web.HTTPMethodNotAllowed(text=json.dumps(error), content_type='application/json')
            else:
                LOG.debug(err)
                error = build_beacon_error_response(500, qparams, str(err))
                raise web.HTTPInternalServerError(text=json.dumps(error), content_type='application/json')
                
        return await json_stream(request, response)

    return wrapper

def filtering_terms_handler(db_fn, request=None):
    async def wrapper(request: Request):
        try:
            # Get params
            json_body = await request.json() if request.method == "POST" and request.has_body and request.can_read_body else {}
            qparams = RequestParams(**json_body).from_request(request)

            #LOG.debug(qparams)
            
            search_datasets = []
            authenticated=False
            access_token = request.headers.get('Authorization')
            #LOG.debug(access_token)
            if access_token is not None:
                try:
                    specific_datasets = qparams.query.request_parameters['datasets']
                except Exception:
                    specific_datasets = []
                access_token = access_token[7:]  # cut out 7 characters: len('Bearer ')

                
                authorized_datasets, authenticated = await resolve_token(access_token, search_datasets)
                ##LOG.debug(authorized_datasets)
                ##LOG.debug('all datasets:  %s', all_datasets)
                LOG.info('resolved datasets:  %s', authorized_datasets)
                ##LOG.debug(authenticated)
                ##LOG.debug(specific_datasets)

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
                    #LOG.debug(specific_search_datasets)
                    #LOG.debug(response_datasets)

                else:
                    qparams.query.request_parameters = {}
                    qparams.query.request_parameters['datasets'] = '*******'
                    _, _, datasets = get_datasets(None, qparams)
                    beacon_datasets = [ r for r in datasets ]
                    specific_datasets = [ r['id'] for r in beacon_datasets if r['id'] not in authorized_datasets]
                    response_datasets = [ r['id'] for r in beacon_datasets if r['id'] in authorized_datasets]
                    ##LOG.debug(specific_datasets)
                    ##LOG.debug(response_datasets)

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
        except Exception as err:
            qparams = ''
            if str(err) == 'Not Found':
                error = build_beacon_error_response(404, qparams, str(err))
                raise web.HTTPNotFound(text=json.dumps(error), content_type='application/json')
            elif str(err) == 'Bad Request':
                error = build_beacon_error_response(400, qparams, str(err))
                raise web.HTTPBadRequest(text=json.dumps(error), content_type='application/json')
            elif str(err) == 'Bad Gateway':
                error = build_beacon_error_response(502, qparams, str(err))
                raise web.HTTPBadGateway(text=json.dumps(error), content_type='application/json')
            elif str(err) == 'Method Not Allowed':
                error = build_beacon_error_response(405, qparams, str(err))
                raise web.HTTPMethodNotAllowed(text=json.dumps(error), content_type='application/json')
            else:
                LOG.debug(err)
                error = build_beacon_error_response(500, qparams, str(err))
                raise web.HTTPInternalServerError(text=json.dumps(error), content_type='application/json')
                
        return await json_stream(request, response)

    return wrapper
