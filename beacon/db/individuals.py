import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query, get_filtering_documents, get_docs_by_response_type, join_query
from beacon.db import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents
from beacon.request.model import RequestParams
import yaml
from aiohttp import web

LOG = logging.getLogger(__name__)


VARIANTS_PROPERTY_MAP = {
    "start": "variation.location.interval.start.value",
    "end": "variation.location.interval.end.value",
    "assemblyId": "identifiers.genomicHGVSId",
    "referenceName": "identifiers.genomicHGVSId",
    "referenceBases": "variation.referenceBases",
    "alternateBases": "variation.alternateBases",
    "variantType": "variation.variantType",
    "variantMinLength": "variantInternalId",
    "variantMaxLength": "variantInternalId",
    "geneId": "molecularAttributes.geneIds",
    "genomicAlleleShortForm": "identifiers.genomicHGVSId",
    "aminoacidChange": "molecularAttributes.aminoacidChanges",
    "clinicalRelevance": "caseLevelData.clinicalInterpretations.clinicalRelevance"
}

def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    return query

def generate_position_filter_start(key: str, value: List[int]) -> List[AlphanumericFilter]:
    #LOG.debug("len value = {}".format(len(value)))
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[0],
            operator=Operator.GREATER_EQUAL
        ))
    elif len(value) == 2:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[0],
            operator=Operator.GREATER_EQUAL
        ))
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[1],
            operator=Operator.LESS_EQUAL
        ))
    return filters


def generate_position_filter_end(key: str, value: List[int]) -> List[AlphanumericFilter]:
    #LOG.debug("len value = {}".format(len(value)))
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[0],
            operator=Operator.LESS_EQUAL
        ))
    elif len(value) == 2:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[0],
            operator=Operator.GREATER_EQUAL
        ))
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[1],
            operator=Operator.LESS_EQUAL
        ))
    return filters

def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    collection = 'g_variants'
    #LOG.debug("Request parameters len = {}".format(len(qparams.query.request_parameters)))
    if len(qparams.query.request_parameters) > 0 and "$and" not in query:
        query["$and"] = []
    if isinstance(qparams.query.request_parameters, list):
        for reqparam in qparams.query.request_parameters:
            subquery={}
            subquery["$and"] = []
            for k, v in reqparam.items():
                if k == "start":
                    if isinstance(v, str):
                        v = v.split(',')
                    filters = generate_position_filter_start(k, v)
                    for filter in filters:
                        subquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                elif k == "end":
                    if isinstance(v, str):
                        v = v.split(',')
                    filters = generate_position_filter_end(k, v)
                    for filter in filters:
                        subquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                elif k == "datasets":
                    pass
                elif k == "variantMinLength":
                    try:
                        subquery["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                            id=VARIANTS_PROPERTY_MAP[k],
                            value='min'+v
                        ), collection))
                    except KeyError:
                        raise web.HTTPNotFound
                elif k == "variantMaxLength":
                    try:
                        subquery["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                            id=VARIANTS_PROPERTY_MAP[k],
                            value='max'+v
                        ), collection))
                    except KeyError:
                        raise web.HTTPNotFound    
                elif k != 'filters':
                    try:
                        subquery["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                            id=VARIANTS_PROPERTY_MAP[k],
                            value=v
                        ), collection))
                    except KeyError:
                        raise web.HTTPNotFound

                elif k == 'filters':
                    v_list=[]
                    if ',' in v:
                        v_list =v.split(',')
                        LOG.debug(v_list)
                    else:
                        v_list.append(v)
                    for id in v_list:
                        v_dict={}
                        v_dict['id']=id
                        qparams.query.filters.append(v_dict)        
                    return query, True
            query["$and"].append(subquery)
    else:
        for k, v in qparams.query.request_parameters.items():
            if k == "start":
                if isinstance(v, str):
                    v = v.split(',')
                filters = generate_position_filter_start(k, v)
                for filter in filters:
                    query["$and"].append(apply_alphanumeric_filter({}, filter, collection))
            elif k == "end":
                if isinstance(v, str):
                    v = v.split(',')
                filters = generate_position_filter_end(k, v)
                for filter in filters:
                    query["$and"].append(apply_alphanumeric_filter({}, filter, collection))
            elif k == "datasets":
                pass
            elif k == "variantMinLength":
                try:
                    query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                        id=VARIANTS_PROPERTY_MAP[k],
                        value='min'+v
                    ), collection))
                except KeyError:
                    raise web.HTTPNotFound
            elif k == "variantMaxLength":
                try:
                    query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                        id=VARIANTS_PROPERTY_MAP[k],
                        value='max'+v
                    ), collection))
                except KeyError:
                    raise web.HTTPNotFound    
            elif k != 'filters':
                try:
                    query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                        id=VARIANTS_PROPERTY_MAP[k],
                        value=v
                    ), collection))
                except KeyError:
                    raise web.HTTPNotFound

            elif k == 'filters':
                v_list=[]
                if ',' in v:
                    v_list =v.split(',')
                    LOG.debug(v_list)
                else:
                    v_list.append(v)
                for id in v_list:
                    v_dict={}
                    v_dict['id']=id
                    qparams.query.filters.append(v_dict)        
                return query, True


    return query, False


def get_individuals(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'individuals'
    mongo_collection = client.beacon.individuals
    parameters_as_filters=False
    query_parameters, parameters_as_filters = apply_request_parameters({}, qparams)
    LOG.debug(query_parameters)
    LOG.debug(parameters_as_filters)
    if parameters_as_filters == True:
        query, parameters_as_filters = apply_request_parameters({}, qparams)
        query_parameters={}
    else:
        query=query_parameters
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
    return schema, count, dataset_count, docs


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
    return schema, count, dataset_count, docs


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
    return schema, count, dataset_count, docs


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
    return schema, count, dataset_count, docs


def get_filtering_terms_of_individual(entry_id: Optional[str], qparams: RequestParams):
    query = {'scope': 'individuals'}
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
    return schema, count, dataset_count, docs

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
    return schema, count, dataset_count, docs
