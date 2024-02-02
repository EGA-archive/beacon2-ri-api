import logging
import yaml
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query
from beacon.db import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import get_documents, query_id, get_count, get_filtering_documents
from beacon.request.model import RequestParams

LOG = logging.getLogger(__name__)

def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    include = qparams.query.include_resultset_responses
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

def get_analyses(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'analyses'
    query = apply_request_parameters({}, qparams)
    LOG.debug(qparams.query.filters)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.ANALYSES
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        query_count=query
        query_count["$or"]=[]
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
                    count=dataset_count
                    if dataset_count == 0:
                        dataset_count=get_count(client.beacon.analyses, {'$or': query_count['$or']})
                        count+=get_count(client.beacon.analyses, {'$or': query_count['$or']})
                        docs = get_documents(
                            client.beacon.analyses,
                            {'$or': query_count['$or']},
                            qparams.query.pagination.skip,
                            10
                        )
                    else:
                        return schema, count, -1, None
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.analyses, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.analyses,
            query,
            qparams.query.pagination.skip,
            10
        )
    elif include == 'HIT':
        count = get_count(client.beacon.analyses, query)
        query_count=query
        i=1
        query_count["$or"]=[]
        for k, v in datasets_dict.items():
            if k == dataset:
                for id in v:
                    LOG.debug(len(v))
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
                        qparams.query.pagination.skip,
                        10
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
                        qparams.query.pagination.skip,
                        10
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs


def get_analysis_with_id(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'analyses'
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.ANALYSES
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        query_count=query
        query_count["$or"]=[]
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
                    count=dataset_count
                    if dataset_count == 0:
                        dataset_count=get_count(client.beacon.analyses, {'$or': query_count['$or']})
                        count+=get_count(client.beacon.analyses, {'$or': query_count['$or']})
                        docs = get_documents(
                            client.beacon.analyses,
                            {'$or': query_count['$or']},
                            qparams.query.pagination.skip,
                            10
                        )
                    else:
                        return schema, count, -1, None
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.analyses, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.analyses,
            query,
            qparams.query.pagination.skip,
            10
        )
    elif include == 'HIT':
        count = get_count(client.beacon.analyses, query)
        query_count=query
        i=1
        query_count["$or"]=[]
        for k, v in datasets_dict.items():
            if k == dataset:
                for id in v:
                    LOG.debug(len(v))
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
                        qparams.query.pagination.skip,
                        10
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
                        qparams.query.pagination.skip,
                        10
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs


def get_variants_of_analysis(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'analyses'
    query = {"$and": [{"id": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.analyses, query)
    analysis_ids = client.beacon.analyses \
        .find_one(query, {"biosampleId": 1, "_id": 0})
    LOG.debug(analysis_ids)
    query = {"caseLevelData.biosampleId": analysis_ids["biosampleId"]}
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.GENOMICVARIATIONS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        query_count=query
        query_count["$or"]=[]
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
                    count=dataset_count
                    if dataset_count == 0:
                        dataset_count=get_count(client.beacon.genomicVariations, {'$or': query_count['$or']})
                        count+=get_count(client.beacon.genomicVariations, {'$or': query_count['$or']})
                        docs = get_documents(
                            client.beacon.genomicVariations,
                            {'$or': query_count['$or']},
                            qparams.query.pagination.skip,
                            10
                        )
                    else:
                        return schema, count, -1, None
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.genomicVariations, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.individuals,
            query,
            qparams.query.pagination.skip,
            10
        )
    elif include == 'HIT':
        count = get_count(client.beacon.genomicVariations, query)
        query_count=query
        i=1
        query_count["$or"]=[]
        for k, v in datasets_dict.items():
            if k == dataset:
                for id in v:
                    LOG.debug(len(v))
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
                        qparams.query.pagination.skip,
                        10
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
                        qparams.query.pagination.skip,
                        10
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs

def get_filtering_terms_of_analyse(entry_id: Optional[str], qparams: RequestParams):
    query = {'scope': 'analyses'}
    schema = DefaultSchemas.FILTERINGTERMS
    count = get_count(client.beacon.filtering_terms, query)
    remove_id={'_id':0}
    docs = get_filtering_documents(
        client.beacon.filtering_terms,
        query,
        remove_id,
        qparams.query.pagination.skip,
        0
    )
    return schema, count, docs

