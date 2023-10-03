import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query, get_filtering_documents
from beacon.db import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents
from beacon.request.model import RequestParams
import json
from bson import json_util

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
    include = qparams.query.include_resultset_responses
    if include == 'HIT':
        query = query
    elif include == 'ALL':
        query = {}
    elif include == 'NONE':
        query = {'$text': {'$search': '########'}}
    else:
        query = query
    return query

def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Request parameters len = {}".format(len(qparams.query.request_parameters)))
    v_list=[]
    query_2={}
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
                qparams.query.pagination.skip,
                count
            )
                biosample_IDS =[]

                query_2["$or"] = []
                for doc in docs:
                    caseLevelData = doc['caseLevelData']
                    for case in caseLevelData:
                        #LOG.debug(case["biosampleId"])
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

                        
                

        
    return query_2


def get_individuals(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = apply_request_parameters({}, qparams)
    LOG.debug(qparams.query.filters)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.INDIVIDUALS
    count = get_count(client.beacon.individuals, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.individuals,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.individuals,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.individuals, negative_query)
    else:
        docs = get_documents(
            client.beacon.individuals,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs


def get_individual_with_id(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.INDIVIDUALS
    count = get_count(client.beacon.individuals, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.individuals,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.individuals,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.individuals, negative_query)
    else:
        docs = get_documents(
            client.beacon.individuals,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs


def get_variants_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"$and": [{"id": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.individuals, query)
    individual_ids = client.beacon.individuals \
        .find_one(query, {"id": 1, "_id": 0})
    LOG.debug(individual_ids)
    individual_ids=get_cross_query(individual_ids,'id','caseLevelData.biosampleId')
    LOG.debug(individual_ids)
    query = apply_filters(individual_ids, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.GENOMICVARIATIONS
    count = get_count(client.beacon.genomicVariations, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.genomicVariations,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.genomicVariations,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.genomicVariations, negative_query)
    else:
        docs = get_documents(
            client.beacon.genomicVariations,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs


def get_biosamples_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.BIOSAMPLES
    count = get_count(client.beacon.biosamples, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.biosamples,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.biosamples,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.biosamples, negative_query)
    else:
        docs = get_documents(
            client.beacon.biosamples,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs


def get_filtering_terms_of_individual(entry_id: Optional[str], qparams: RequestParams):
    query = {'scope': 'individuals'}
    schema = DefaultSchemas.FILTERINGTERMS
    count = get_count(client.beacon.filtering_terms, query)
    remove_id={'_id':0}
    docs = get_filtering_documents(
        client.beacon.filtering_terms,
        query,
        remove_id,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_runs_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.RUNS
    count = get_count(client.beacon.runs, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.runs,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.runs,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.runs, negative_query)
    else:
        docs = get_documents(
            client.beacon.runs,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs

def get_analyses_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.ANALYSES
    count = get_count(client.beacon.analyses, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.analyses,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.analyses,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.analyses, negative_query)
    else:
        docs = get_documents(
            client.beacon.analyses,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs
