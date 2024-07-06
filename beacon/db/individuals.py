import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query, get_filtering_documents, get_docs_by_response_type, join_query
from beacon.db import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents
from beacon.request.model import RequestParams
from beacon.db.g_variants import apply_request_parameters
import time
import yaml
from aiohttp import web

LOG = logging.getLogger(__name__)

def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    return query

def get_individuals(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    LOG.debug(time.time())
    collection = 'individuals'
    mongo_collection = client.beacon.individuals
    parameters_as_filters=False
    query_parameters, parameters_as_filters = apply_request_parameters({}, qparams)
    LOG.debug(query_parameters)
    LOG.debug(parameters_as_filters)
    if parameters_as_filters == True and query_parameters != {'$and': []}:
        query, parameters_as_filters = apply_request_parameters({}, qparams)
        query_parameters={}
    elif query_parameters != {'$and': []}:
        query=query_parameters
    elif query_parameters == {'$and': []}:
        query_parameters = {}
        query={}
    query = apply_filters(query, qparams.query.filters, collection, query_parameters)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.INDIVIDUALS
    #with open("beacon/request/datasets.yml", 'r') as datasets_file:
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


def get_individual_with_id(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'individuals'
    idq="id"
    mongo_collection = client.beacon.individuals
    query, parameters_as_filters = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection, {})
    query = query_id(query, entry_id)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.INDIVIDUALS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs, dataset


def get_variants_of_individual(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    query = {"individualId": entry_id}
    mongo_collection = client.beacon.biosamples
    excluding_fields={"_id": 0, "id": 1}
    biosampleId=mongo_collection.find(query, excluding_fields)
    query = {"caseLevelData.biosampleId": biosampleId[0]["id"]}
    mongo_collection = client.beacon.genomicVariations
    query, parameters_as_filters = apply_request_parameters(query, qparams)
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


def get_biosamples_of_individual(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'biosamples'
    mongo_collection = client.beacon.biosamples
    query = {"individualId": entry_id}
    query, parameters_as_filters = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection, {})
    query = include_resultset_responses(query, qparams)
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


def get_filtering_terms_of_individual(entry_id: Optional[str], qparams: RequestParams):
    query = {'scopes': 'individual'}
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


def get_runs_of_individual(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'individuals'
    mongo_collection = client.beacon.runs
    query = {"individualId": entry_id}
    query, parameters_as_filters = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection, {})
    query = include_resultset_responses(query, qparams)
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

def get_analyses_of_individual(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'individuals'
    mongo_collection = client.beacon.analyses
    query = {"individualId": entry_id}
    query, parameters_as_filters = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection, {})
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.ANALYSES
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
