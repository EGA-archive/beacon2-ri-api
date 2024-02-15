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

LOG = logging.getLogger(__name__)


VARIANTS_PROPERTY_MAP = {
    "assemblyId": "_position.assemblyId",
    "Chromosome": "_position.refseqId",
    "start": "_position.start",
    "end": "_position.end",
    "referenceBases": "variation.referenceBases",
    "alternateBases": "variation.alternateBases",
    "variantType": "variation.variantType",
    "variantMinLength": None,
    "variantMaxLength": None,
    "mateName": None,
    "gene": "molecularAttributes.geneIds",
    "aachange": "molecularAttributes.aminoacidChanges"
}


def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    return query

def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Request parameters len = {}".format(len(qparams.query.request_parameters)))
    v_list=[]
    query_2={}
    limit = qparams.query.pagination.limit
    for k, v in qparams.query.request_parameters.items():
        LOG.debug(k)
        
        if k == 'filters':
            if 'genomicVariations' in v:
                LOG.debug("yes")
                listing = v.split('"')
                value_list = listing[1].split('.')
                value_equal = value_list[1]
                final_list = value_equal.split('=')
                final_value = final_list[1]
                query["$and"] = []
                collection = 'g_variants'
                query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                    id=VARIANTS_PROPERTY_MAP[final_list[0]],
                    value=final_value
                ), collection))
                count = get_count(client.beacon.genomicVariations, query)
                docs = get_documents(
                client.beacon.genomicVariations,
                query,
                qparams.query.pagination.skip*limit,
                count
            )
                biosample_IDS =[]
                query_2["$or"] = []
                for doc in docs:
                    caseLevelData = doc['caseLevelData']
                    for case in caseLevelData:
                        if case["biosampleId"] not in biosample_IDS:
                            biosample_IDS.append(case["biosampleId"])
                            query_2["$or"].append({'id': case["biosampleId"]})

                LOG.debug(query_2)
                
            elif ',' in v:
                v_list =v.split(',')
                LOG.debug(v_list)
            else:
                v_list.append(v)
            for id in v_list:
                v_dict={}
                v_dict['id']=id
                qparams.query.filters.append(v_dict)        
    if query_2 != {}:  
        return query_2
    else:
        return query


def get_individuals(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'individuals'
    mongo_collection = client.beacon.individuals
    query = apply_request_parameters({}, qparams)
    match_list=[]
    matching = apply_request_parameters({}, qparams)
    match_list.append(matching)
    match_big={}
    match_big["$match"]=match_list[0]
    LOG.debug(qparams.query.filters)
    query = apply_filters(query, qparams.query.filters, collection)
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
    try:
        aggregation_string_list=query['$and']
    except Exception:
        aggregation_string_list=[]
    LOG.debug(aggregation_string_list)
    if aggregation_string_list != []:
        if isinstance(aggregation_string_list[0], str):
            string_list=aggregation_string_list[0].split(' ')
            filter_id=qparams.query.filters[0]["id"]
            if 'aggregate' in aggregation_string_list[0]:
                count, dataset_count, docs = join_query(string_list, filter_id, match_big, qparams, idq, datasets_dict, dataset, mongo_collection)
        else:
            count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    else:
        count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs


def get_individual_with_id(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'individuals'
    idq="id"
    mongo_collection = client.beacon.individuals
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
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
    mongo_collection = client.beacon.genomicVariations
    query = {"caseLevelData.biosampleId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
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
    LOG.debug(query)
    query = apply_request_parameters(query, qparams)
    LOG.debug(query)
    query = apply_filters(query, qparams.query.filters, collection)
    LOG.debug(query)
    query = include_resultset_responses(query, qparams)
    LOG.debug(query)
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
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
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
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
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
