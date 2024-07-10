from typing import Optional
from typing import Dict, List, Optional
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents, get_cross_query, get_docs_by_response_type
from beacon.request.model import RequestParams
from beacon.db import client
from beacon import conf

import logging
import yaml

LOG = logging.getLogger(__name__)

def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    #LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    return query

def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    #LOG.debug("Request parameters len = {}".format(len(qparams.query.request_parameters)))
    for k, v in qparams.query.request_parameters.items():
        if ',' in v:
            query["$text"] = {}
            v_list = v.split(',')
            v_string=''
            for val in v_list:
                v_string += f'"{val}"'
            query["$text"]["$search"]=v_string
        elif k == 'datasets':
            if v == '*******':
                query = {}
            else:
                query["$text"] = {}
                string = ''
                for word in v:
                    string = word + ' '
                dict_search={}
                dict_search['$search']=string
                query["$text"]=dict_search
                
        else:
            query["$text"] = {}
            dict_search={}
            dict_search['$search']=v
            query["$text"]=dict_search
    #LOG.debug(query)
    return query

def get_datasets(entry_id: Optional[str], qparams: RequestParams):
    collection = 'datasets'
    limit = qparams.query.pagination.limit
    query = apply_request_parameters({}, qparams)
    #query = apply_filters({}, qparams.query.filters, collection)
    schema = DefaultSchemas.DATASETS
    count = get_count(client.beacon.datasets, query)
    docs = get_documents(
        client.beacon.datasets,
        query,
        0,
        qparams.query.pagination.skip*limit
    )
    return schema, count, docs


def get_dataset_with_id(entry_id: Optional[str], qparams: RequestParams):
    collection = 'datasets'
    dataset_count=1
    limit = qparams.query.pagination.limit
    query = apply_request_parameters({}, qparams)
    #query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    schema = DefaultSchemas.DATASETS
    count = get_count(client.beacon.datasets, query)
    docs = get_documents(
        client.beacon.datasets,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.skip*limit
    )
    return schema, count, docs

def get_variants_of_biosample(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.genomicVariations
    query = {"caseLevelData.biosampleId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection, {})
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.GENOMICVARIATIONS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    idq="caseLevelData.biosampleId"
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs, dataset


def get_variants_of_dataset(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'datasets'
    mongo_collection = client.beacon.genomicVariations
    dataset_count=0
    limit = qparams.query.pagination.limit
    #query = apply_filters({}, qparams.query.filters, collection)
    #query = query_id(query, entry_id)
    #count = get_count(client.beacon.datasets, query)
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    query_count={}
    idq="caseLevelData.biosampleId"
    i=1
    LOG.debug(entry_id)
    query_count["$or"]=[]
    if dataset == entry_id:
        for k, v in datasets_dict.items():
            if k == entry_id and k == dataset:
                LOG.debug(v)
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid[idq]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid[idq]=id
                        query_count["$or"].append(queryid)
                        i=1
    else:
        schema = DefaultSchemas.GENOMICVARIATIONS
        return schema, 0, -1, None
    query = apply_filters(query_count, qparams.query.filters, collection, {})
    schema = DefaultSchemas.GENOMICVARIATIONS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs, dataset


def get_biosamples_of_dataset(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'datasets'
    mongo_collection = client.beacon.biosamples
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection, {})
    query = query_id(query, entry_id)
    count = get_count(client.beacon.datasets, query)
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    biosample_ids=get_cross_query(datasets_dict[entry_id],'biosampleIds','id')
    query = apply_filters(biosample_ids, qparams.query.filters, collection, {})
    #LOG.debug(query)
    schema = DefaultSchemas.BIOSAMPLES
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    idq="id"
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs, dataset


def get_individuals_of_dataset(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'datasets'
    mongo_collection = client.beacon.individuals
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection, {})
    query = query_id(query, entry_id)
    count = get_count(client.beacon.datasets, query)
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    individual_ids=get_cross_query(datasets_dict[entry_id],'individualIds','id')
    query = apply_filters(individual_ids, qparams.query.filters, collection, {})
    schema = DefaultSchemas.INDIVIDUALS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    idq="id"
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs, dataset


def filter_public_datasets(requested_datasets_ids):
    query = {"dataUseConditions.duoDataUse.modifiers.id": "DUO:0000004"}
    return client.beacon.datasets \
        .find(query)


def get_filtering_terms_of_dataset(entry_id: Optional[str], qparams: RequestParams):
    query = {'scopes': 'dataset'}
    schema = DefaultSchemas.FILTERINGTERMS
    count = get_count(client.beacon.filtering_terms, query)
    docs = get_documents(
        client.beacon.filtering_terms,
        query,
        qparams.query.pagination.skip,
        0
    )
    return schema, count, docs


def get_runs_of_dataset(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'datasets'
    mongo_collection = client.beacon.runs
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection, {})
    query = query_id(query, entry_id)
    count = get_count(client.beacon.datasets, query)
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    biosample_ids=get_cross_query(datasets_dict[entry_id],'biosampleIds','biosampleId')
    LOG.debug(biosample_ids)
    query = apply_filters(biosample_ids, qparams.query.filters, collection, {})
    schema = DefaultSchemas.RUNS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    idq="biosampleId"
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs, dataset


def get_analyses_of_dataset(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'datasets'
    idq="biosampleId"
    mongo_collection = client.beacon.analyses
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection, {})
    query = query_id(query, entry_id)
    count = get_count(client.beacon.datasets, query)
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    biosample_ids=get_cross_query(datasets_dict[entry_id],'biosampleIds','biosampleId')
    query = apply_filters(biosample_ids, qparams.query.filters, collection, {})
    schema = DefaultSchemas.ANALYSES
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs

def beacon_handovers():
    query = {}
    docs = get_documents(
        client.beacon.datasets,
        query,
        0,
        100
    )
    beacon_handovers=[]
    for doc in docs:
        try:
            note = doc["description"]
        except Exception:
            note = ""
        try:
            url = doc["externalUrl"]
        except Exception:
            url = ""
        if doc["id"] == "coadread_tcga_pan_can_atlas_2018":
            beacon_handovers.append(
            {
                'handoverType': {
                    'id': 'NCIT:C189151',
                    'label': 'Study Data Repository'
                },
                'note': note,
                'url': url
            }
            )
        else:
            beacon_handovers.append(conf.beacon_handovers)
    return beacon_handovers

def beacon_handovers_by_dataset(dataset: str):
    query = {"id": dataset}
    docs = get_documents(
        client.beacon.datasets,
        query,
        0,
        1
    )
    beacon_handovers=[]
    for doc in docs:
        try:
            note = doc["description"]
        except Exception:
            note = ""
        try:
            url = doc["externalUrl"]
        except Exception:
            url = ""
        if doc["id"] == "coadread_tcga_pan_can_atlas_2018":
            beacon_handovers=[
            {
                'handoverType': {
                    'id': 'NCIT:C189151',
                    'label': 'Study Data Repository'
                },
                'note': note,
                'url': url
            }
            ]
        else:
            beacon_handovers=conf.beacon_handovers
    return beacon_handovers
