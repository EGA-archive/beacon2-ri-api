import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, query_ids, get_count, get_documents, join_query, get_filtering_documents, get_aggregated_documents, get_docs_by_response_type
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db import client
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
    #LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
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
        else:
            try:
                query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                    id=VARIANTS_PROPERTY_MAP[k],
                    value=v
                ), collection))
            except KeyError:
                raise web.HTTPNotFound
    return query


def get_variants(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.genomicVariations
    query = apply_request_parameters({}, qparams)
    LOG.debug(query)
    query = apply_filters(query, qparams.query.filters, collection,{})
    LOG.debug(query)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.GENOMICVARIATIONS
    idq="caseLevelData.biosampleId"
    #with open("beacon/request/datasets.yml", 'r') as datasets_file:
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    #LOG.debug(query)
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs


def get_variant_with_id(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.genomicVariations
    query = {"$and": [{"variantInternalId": entry_id}]}
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
    return schema, count, dataset_count, docs


def get_biosamples_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.biosamples
    query = {"$and": [{"variantInternalId": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = query = apply_filters(query, qparams.query.filters, collection, {})
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosampleId": 1, "_id": 0})
    biosample_id=biosample_ids["caseLevelData"]
    try:
        finalid=biosample_id[0]["biosampleId"]
    except Exception:
        finalid=biosample_id["biosampleId"]
    query = {"id": finalid}
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

def get_runs_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.runs
    query = {"$and": [{"variantInternalId": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = query = apply_filters(query, qparams.query.filters, collection, {})
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosampleId": 1, "_id": 0})
    biosample_id=biosample_ids["caseLevelData"]
    try:
        finalid=biosample_id[0]["biosampleId"]
    except Exception:
        finalid=biosample_id["biosampleId"]
    query = {"biosampleId": finalid}
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


def get_analyses_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.analyses
    query = {"$and": [{"variantInternalId": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = query = apply_filters(query, qparams.query.filters, collection, {})
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosampleId": 1, "_id": 0})
    biosample_id=biosample_ids["caseLevelData"]
    try:
        finalid=biosample_id[0]["biosampleId"]
    except Exception:
        finalid=biosample_id["biosampleId"]
    query = {"biosampleId": finalid}
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

def get_filtering_terms_of_genomicvariation(entry_id: Optional[str], qparams: RequestParams):
    query = {'scope': 'genomicVariations'}
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

def get_individuals_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.individuals
    query = {"$and": [{"variantInternalId": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = query = apply_filters(query, qparams.query.filters, collection, {})
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosampleId": 1, "_id": 0})
    biosample_id=biosample_ids["caseLevelData"]
    try:
        finalid=biosample_id[0]["biosampleId"]
    except Exception:
        finalid=biosample_id["biosampleId"]
    query = {"id": finalid}
    query = apply_filters(query, qparams.query.filters, collection, {})
    query = include_resultset_responses(query, qparams)
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
    return schema, count, dataset_count, docs