import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query, get_cross_query_variants, get_filtering_documents
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
    "aminoacidChange": "molecularAttributes.aminoacidChanges"
}

def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    return query


def generate_position_filter_start(key: str, value: List[int]) -> List[AlphanumericFilter]:
    LOG.debug("len value = {}".format(len(value)))
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
    LOG.debug("len value = {}".format(len(value)))
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
    LOG.debug("Request parameters len = {}".format(len(qparams.query.request_parameters)))
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
    query = apply_request_parameters({}, qparams)
    LOG.debug(qparams.query.filters)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.GENOMICVARIATIONS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 1000 or limit == 0:
        limit = 1000
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
                            limit
                        )
                    else:
                        return schema, count, -1, None
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.genomicVariations, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.genomicVariations,
            query,
            qparams.query.pagination.skip,
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
                        qparams.query.pagination.skip,
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
                        qparams.query.pagination.skip,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs


def get_variant_with_id(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    query = {"$and": [{"variantInternalId": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.GENOMICVARIATIONS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 1000 or limit == 0:
        limit = 1000
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
                            limit
                        )
                    else:
                        return schema, count, -1, None
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.genomicVariations, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.genomicVariations,
            query,
            qparams.query.pagination.skip,
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
                        qparams.query.pagination.skip,
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
                        qparams.query.pagination.skip,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs


def get_biosamples_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    query = {"$and": [{"variantInternalId": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.genomicVariations, query)
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosampleId": 1, "_id": 0})
    biosample_id=biosample_ids["caseLevelData"]
    finalid=biosample_id[0]["biosampleId"]
    query = {"id": finalid}
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.BIOSAMPLES
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 1000 or limit == 0:
        limit = 1000
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
                    count=dataset_count
                    if dataset_count == 0:
                        dataset_count=get_count(client.beacon.biosamples, {'$or': query_count['$or']})
                        count+=get_count(client.beacon.biosamples, {'$or': query_count['$or']})
                        docs = get_documents(
                            client.beacon.biosamples,
                            {'$or': query_count['$or']},
                            qparams.query.pagination.skip,
                            limit
                        )
                    else:
                        return schema, count, -1, None
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.biosamples, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.biosamples,
            query,
            qparams.query.pagination.skip,
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
                        qparams.query.pagination.skip,
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
                        qparams.query.pagination.skip,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs

def get_runs_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    query = {"$and": [{"variantInternalId": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.genomicVariations, query)
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosampleId": 1, "_id": 0})
    biosample_id=biosample_ids["caseLevelData"]
    finalid=biosample_id[0]["biosampleId"]
    query = {"biosampleId": finalid}
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.RUNS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 1000 or limit == 0:
        limit = 1000
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
                    dataset_count = get_count(client.beacon.runs, query_count)
                    count=dataset_count
                    if dataset_count == 0:
                        dataset_count=get_count(client.beacon.runs, {'$or': query_count['$or']})
                        count+=get_count(client.beacon.runs, {'$or': query_count['$or']})
                        docs = get_documents(
                            client.beacon.runs,
                            {'$or': query_count['$or']},
                            qparams.query.pagination.skip,
                            limit
                        )
                    else:
                        return schema, count, -1, None
                else:
                    dataset_count=0

    elif include == 'NONE':
            count = get_count(client.beacon.runs, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.runs,
            query,
            qparams.query.pagination.skip,
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
                        qparams.query.pagination.skip,
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
                        qparams.query.pagination.skip,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs


def get_analyses_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    query = {"$and": [{"variantInternalId": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.genomicVariations, query)
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosampleId": 1, "_id": 0})
    biosample_id=biosample_ids["caseLevelData"]
    finalid=biosample_id[0]["biosampleId"]
    query = {"biosampleId": finalid}
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.ANALYSES
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 1000 or limit == 0:
        limit = 1000
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
                            limit
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
                        qparams.query.pagination.skip,
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
                        qparams.query.pagination.skip,
                        limit
                    )
                else:
                    dataset_count=0
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
        qparams.query.pagination.skip,
        0
    )
    return schema, count, docs

def get_individuals_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    query = {"$and": [{"variantInternalId": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.genomicVariations, query)
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosampleId": 1, "_id": 0})
    biosample_id=biosample_ids["caseLevelData"]
    finalid=biosample_id[0]["biosampleId"]
    query = {"id": finalid}
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.INDIVIDUALS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 1000 or limit == 0:
        limit = 1000
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
                        queryid["id"]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid["id"]=id
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
                            limit
                        )
                    else:
                        return schema, count, -1, None
                else:
                    dataset_count=0
    elif include == 'NONE':
            count = get_count(client.beacon.individuals, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.analyses,
            query,
            qparams.query.pagination.skip,
            limit
        )
    elif include == 'HIT':
        count = get_count(client.beacon.individuals, query)
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
                    dataset_count = get_count(client.beacon.individuals, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.individuals,
                        query_count,
                        qparams.query.pagination.skip,
                        limit
                    )
                else:
                    dataset_count=0
        if dataset_count==0:
            return schema, count, -1, None
    elif include == 'ALL':
        count = get_count(client.beacon.individuals, query)
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
                    dataset_count = get_count(client.beacon.individuals, query_count)
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.individuals,
                        query_count,
                        qparams.query.pagination.skip,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs