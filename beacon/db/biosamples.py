import logging
import yaml
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query, get_filtering_documents
from beacon.db import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db.filters import *
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import *
from beacon.request.model import RequestParams

LOG = logging.getLogger(__name__)

def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    return query

def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Request parameters len = {}".format(len(qparams.query.request_parameters)))
    for k, v in qparams.query.request_parameters.items():
        query["$text"] = {}
        if ',' in v:
            v_list = v.split(',')
            v_string=''
            for val in v_list:
                v_string += f'"{val}"'
            query["$text"]["$search"]=v_string
        else:
            query["$text"]["$search"]=v
    return query


def get_biosamples(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'biosamples'
    query = apply_request_parameters({}, qparams)
    LOG.debug(qparams.query.filters)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.BIOSAMPLES
    #with open("beacon/request/datasets.yml", 'r') as datasets_file:
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 100 or limit == 0:
        limit = 100
    if include == 'MISS':
        count = get_count(client.beacon.biosamples, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.biosamples, query_count)
                    if dataset_count!=0:
                        return schema, count, -1, None
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.biosamples,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.biosamples, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.biosamples,
            query,
            qparams.query.pagination.skip*limit,
            limit
        )
    elif include == 'HIT':
        count = get_count(client.beacon.biosamples, query)
        query_count=query
        i=1
        query_count["$or"]=[]
        for k, v in datasets_dict.items():
            if k == dataset:
                for id in v:
                    
                    if i < len(v):
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.biosamples, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.biosamples,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
        if dataset_count==0:
            return schema, count, -1, None
    elif include == 'ALL':
        count = get_count(client.beacon.biosamples, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.biosamples, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.biosamples,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs


def get_biosample_with_id(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'biosamples'
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.BIOSAMPLES
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 100 or limit == 0:
        limit = 100
    if include == 'MISS':
        count = get_count(client.beacon.biosamples, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.biosamples, query_count)
                    if dataset_count!=0:
                        return schema, count, -1, None
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.biosamples,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.biosamples, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.biosamples,
            query,
            qparams.query.pagination.skip*limit,
            limit
        )
    elif include == 'HIT':
        count = get_count(client.beacon.biosamples, query)
        query_count=query
        i=1
        query_count["$or"]=[]
        for k, v in datasets_dict.items():
            if k == dataset:
                for id in v:
                    
                    if i < len(v):
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.biosamples, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.biosamples,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
        if dataset_count==0:
            return schema, count, -1, None
    elif include == 'ALL':
        count = get_count(client.beacon.biosamples, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.biosamples, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.biosamples,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs

def get_variants_of_biosample(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    query = {"caseLevelData.biosampleId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.GENOMICVARIATIONS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 100 or limit == 0:
        limit = 100
    if include == 'MISS':
        count = get_count(client.beacon.genomicVariations, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["caseLevelData.biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["caseLevelData.biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.genomicVariations, query_count)
                    if dataset_count!=0:
                        return schema, count, -1, None
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.genomicVariations,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.genomicVariations, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.genomicVariations,
            query,
            qparams.query.pagination.skip*limit,
            limit
        )
    elif include == 'HIT':
        count = get_count(client.beacon.genomicVariations, query)
        query_count=query
        i=1
        query_count["$or"]=[]
        for k, v in datasets_dict.items():
            if k == dataset:
                for id in v:
                    
                    if i < len(v):
                        queryid={}
                        queryid["caseLevelData.biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["caseLevelData.biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.genomicVariations, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.genomicVariations,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
        if dataset_count==0:
            return schema, count, -1, None
    elif include == 'ALL':
        count = get_count(client.beacon.genomicVariations, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["caseLevelData.biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["caseLevelData.biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.genomicVariations, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.genomicVariations,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs


def get_analyses_of_biosample(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'biosamples'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.ANALYSES
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 100 or limit == 0:
        limit = 100
    if include == 'MISS':
        count = get_count(client.beacon.analyses, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.analyses, query_count)
                    LOG.debug(dataset_count)
                    if dataset_count!=0:
                        return schema, count, -1, None
                    docs = get_documents(
                        client.beacon.analyses,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.analyses, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.analyses,
            query,
            qparams.query.pagination.skip*limit,
            limit
        )
    elif include == 'HIT':
        count = get_count(client.beacon.analyses, query)
        query_count=query
        i=1
        query_count["$or"]=[]
        for k, v in datasets_dict.items():
            if k == dataset:
                for id in v:
                    
                    if i < len(v):
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.analyses, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.analyses,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
        if dataset_count==0:
            return schema, count, -1, None
    elif include == 'ALL':
        count = get_count(client.beacon.analyses, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.analyses, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.analyses,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs

def get_runs_of_biosample(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'biosamples'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.RUNS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 100 or limit == 0:
        limit = 100
    if include == 'MISS':
        count = get_count(client.beacon.runs, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.runs, query_count)
                    LOG.debug(dataset_count)
                    if dataset_count!=0:
                        return schema, count, -1, None
                    docs = get_documents(
                        client.beacon.runs,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.runs, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.runs,
            query,
            qparams.query.pagination.skip*limit,
            limit
        )
    elif include == 'HIT':
        count = get_count(client.beacon.runs, query)
        query_count=query
        i=1
        query_count["$or"]=[]
        for k, v in datasets_dict.items():
            if k == dataset:
                for id in v:
                    
                    if i < len(v):
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.runs, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.runs,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
        if dataset_count==0:
            return schema, count, -1, None
    elif include == 'ALL':
        count = get_count(client.beacon.runs, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["biosampleId"]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(client.beacon.runs, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.runs,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs

def get_filtering_terms_of_biosample(entry_id: Optional[str], qparams: RequestParams):
    query = {'scope': 'biosamples'}
    schema = DefaultSchemas.FILTERINGTERMS
    count = get_count(client.beacon.filtering_terms, query)
    remove_id={'_id':0}
    docs = get_filtering_documents(
        client.beacon.filtering_terms,
        query,
        remove_id,
        qparams.query.pagination.skip*qparams.query.pagination.limit,
        0
    )
    return schema, count, docs