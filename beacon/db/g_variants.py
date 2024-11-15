import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, query_ids, get_count, get_documents, join_query, get_filtering_documents, get_aggregated_documents, get_docs_by_response_type
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.db import client
import yaml
import time
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
    "clinicalRelevance": "caseLevelData.clinicalInterpretations.clinicalRelevance",
    "mateName": "identifiers.genomicHGVSId"
}

def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    #LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    return query

def generate_position_filter_start(key: str, value: List[int]) -> List[AlphanumericFilter]:
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[0],
            operator=Operator.GREATER_EQUAL
        ))
    elif len(value) == 2:# pragma: no cover
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

def generate_position_filter_start_2(key: str, value: List[int]) -> List[AlphanumericFilter]:
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP["end"],
            value=value[0],
            operator=Operator.GREATER_EQUAL
        ))
    elif len(value) == 2:# pragma: no cover
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

def generate_position_filter_start_3(key: str, value: List[int]) -> List[AlphanumericFilter]:
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[0],
            operator=Operator.LESS_EQUAL
        ))
    elif len(value) == 2:# pragma: no cover
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
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[0],
            operator=Operator.LESS
        ))
    elif len(value) == 2:# pragma: no cover
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

def generate_position_filter_end_2(key: str, value: List[int]) -> List[AlphanumericFilter]:
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP["start"],
            value=value[0],
            operator=Operator.LESS
        ))
    elif len(value) == 2:# pragma: no cover
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

def generate_position_filter_end_3(key: str, value: List[int]) -> List[AlphanumericFilter]:
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[0],
            operator=Operator.GREATER_EQUAL
        ))
    elif len(value) == 2:# pragma: no cover
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

def generate_position_filter_start_sequence_query(key: str, value: List[int]) -> List[AlphanumericFilter]:
    filters = []
    if len(value) == 1:
        filters.append(AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[key],
            value=value[0],
            operator=Operator.EQUAL
        ))
    return filters

def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    collection = 'g_variants'
    if len(qparams.query.request_parameters) > 0 and "$and" not in query:
        query["$and"] = []
    if isinstance(qparams.query.request_parameters, list):# pragma: no cover
        query={}
        query["$or"]=[]
        for reqparam in qparams.query.request_parameters:
            subquery={}
            subquery["$and"] = []
            startquery={}
            startquery["$and"] = []
            endquery={}
            endquery["$and"] = []
            startendquery={}
            startendquery["$and"] = []
            subqueryor={}
            subqueryor["$or"] = []
            equal=True
            for k, v in reqparam.items():
                if k == 'end':
                    equal=False
            for k, v in reqparam.items():
                if k == "start":
                    if isinstance(v, str):
                        v = v.split(',')
                    if equal == True:
                        filters = generate_position_filter_start_sequence_query(k, v)
                    else:
                        filters = generate_position_filter_start(k, v)
                    for filter in filters:
                        if filter.id == "start":
                            filter[id]=VARIANTS_PROPERTY_MAP["start"]
                            startquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                        elif filter.id == "start2":
                            filter[id]=VARIANTS_PROPERTY_MAP["start"]
                            startquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                        elif filter.id == "start3":
                            filter[id]=VARIANTS_PROPERTY_MAP["start"]
                            startendquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                elif k == "end":
                    if isinstance(v, str):
                        v = v.split(',')
                    filters = generate_position_filter_end(k, v)
                    for filter in filters:
                        if filter.id == "end":
                            filter[id]=VARIANTS_PROPERTY_MAP["end"]
                            endquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                        elif filter.id == "end2":
                            filter[id]=VARIANTS_PROPERTY_MAP["end"]
                            endquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                        elif filter.id == "end3":
                            filter[id]=VARIANTS_PROPERTY_MAP["end"]
                            startendquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
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
                elif k == "mateName" or k == 'referenceName':
                    try:
                        subqueryor["$or"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
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
                    else:
                        v_list.append(v)
                    for id in v_list:
                        v_dict={}
                        v_dict['id']=id
                        qparams.query.filters.append(v_dict)        
                    return query, True
        try:
            if subqueryor["$or"] != []:
                subquery["$and"].append(subqueryor)
            if startquery["$and"] != []:
                subquery["$or"].append(startquery)
            if endquery["$and"] != []:
                subquery["$or"].append(endquery)
            if startendquery["$and"] != []:
                subquery["$or"].append(startendquery)
        except Exception:
            pass
        query["$or"].append(subquery)
    else:
        subquery={}
        subquery["$and"] = []
        subqueryor={}
        subqueryor["$or"] = []
        startquery={}
        startquery["$and"] = []
        endquery={}
        endquery["$and"] = []
        startendquery={}
        startendquery["$and"] = []
        equal=False
        for k, v in qparams.query.request_parameters.items():
            if k == 'end':
                equal=True
        for k, v in qparams.query.request_parameters.items():
            if k == "start":
                if isinstance(v, str):
                    v = v.split(',')
                if equal == False:
                    filters = generate_position_filter_start_sequence_query(k, v)
                    for filter in filters:
                        query["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                else:
                    filters = generate_position_filter_start(k, v)
                    filters2=generate_position_filter_start_2(k, v)
                    filters3=generate_position_filter_start_3(k, v)
                    for filter in filters:
                        startquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                    for filter in filters2:
                        endquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                    for filter in filters3:
                        startendquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
            elif k == "end":
                if isinstance(v, str):
                    v = v.split(',')
                filters = generate_position_filter_end(k, v)
                filters2 = generate_position_filter_end_2(k, v)
                filters3 = generate_position_filter_end_3(k, v)
                for filter in filters:
                    endquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                for filter in filters2:
                    startquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
                for filter in filters3:
                    startendquery["$and"].append(apply_alphanumeric_filter({}, filter, collection))
            elif k == "datasets":
                pass
            elif k == "variantMinLength":
                try:
                    query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                        id=VARIANTS_PROPERTY_MAP[k],
                        value='min'+v
                    ), collection))
                except KeyError:# pragma: no cover
                    raise web.HTTPNotFound
            elif k == "variantMaxLength":
                try:
                    query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                        id=VARIANTS_PROPERTY_MAP[k],
                        value='max'+v
                    ), collection))
                except KeyError:# pragma: no cover
                    raise web.HTTPNotFound    
            elif k == "mateName" or k == 'referenceName':
                try:
                    subqueryor["$or"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                        id=VARIANTS_PROPERTY_MAP[k],
                        value=v
                    ), collection))
                except KeyError:# pragma: no cover
                    raise web.HTTPNotFound
            elif k != 'filters':
                try:
                    query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                        id=VARIANTS_PROPERTY_MAP[k],
                        value=v
                    ), collection))
                except KeyError:# pragma: no cover
                    raise web.HTTPNotFound

            elif k == 'filters':
                v_list=[]
                if ',' in v:
                    v_list =v.split(',')# pragma: no cover
                else:
                    v_list.append(v)
                for id in v_list:
                    v_dict={}
                    v_dict['id']=id
                    qparams.query.filters.append(v_dict)        
                return query, True
        try:
            if subqueryor["$or"] != []:
                subquery["$and"].append(subqueryor)
        except Exception:# pragma: no cover
            pass
        if subquery["$and"] != []:
            query["$and"].append(subquery)
        if startquery["$and"] != []:
            try:
                query["$or"].append(startquery)
            except Exception:
                query["$or"]=[]
                query["$or"].append(startquery)
        if endquery["$and"] != []:
            try:
                query["$or"].append(endquery)
            except Exception:
                query["$or"]=[]
                query["$or"].append(endquery)
        if startendquery["$and"] != []:
            try:
                query["$or"].append(startendquery)
            except Exception:
                query["$or"]=[]
                query["$or"].append(startendquery)


    return query, False


def get_variants(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    LOG.debug(time.time())
    collection = 'g_variants'
    mongo_collection = client.beacon.genomicVariations
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
    query = apply_filters(query, qparams.query.filters, collection,query_parameters)
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
    LOG.debug(time.time())
    return schema, count, dataset_count, docs, dataset


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
    return schema, count, dataset_count, docs, dataset


def get_biosamples_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.biosamples
    query = {"$and": [{"variantInternalId": entry_id}]}
    query_parameters, parameters_as_filters = apply_request_parameters({}, qparams)
    LOG.debug(query_parameters)
    LOG.debug(parameters_as_filters)
    if parameters_as_filters == True:
        query, parameters_as_filters = apply_request_parameters({}, qparams)
        query_parameters={}
    else:
        query=query_parameters
    query = apply_filters(query, qparams.query.filters, collection,query_parameters)
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
    return schema, count, dataset_count, docs, dataset

def get_runs_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.runs
    query = {"$and": [{"variantInternalId": entry_id}]}
    query_parameters, parameters_as_filters = apply_request_parameters({}, qparams)
    LOG.debug(query_parameters)
    LOG.debug(parameters_as_filters)
    if parameters_as_filters == True:
        query, parameters_as_filters = apply_request_parameters({}, qparams)
        query_parameters={}
    else:
        query=query_parameters
    query = apply_filters(query, qparams.query.filters, collection,query_parameters)
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
    return schema, count, dataset_count, docs, dataset


def get_analyses_of_variant(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'g_variants'
    mongo_collection = client.beacon.analyses
    query = {"$and": [{"variantInternalId": entry_id}]}
    query_parameters, parameters_as_filters = apply_request_parameters({}, qparams)
    LOG.debug(query_parameters)
    LOG.debug(parameters_as_filters)
    if parameters_as_filters == True:
        query, parameters_as_filters = apply_request_parameters({}, qparams)
        query_parameters={}
    else:
        query=query_parameters
    query = apply_filters(query, qparams.query.filters, collection,query_parameters)
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
    return schema, count, dataset_count, docs, dataset

def get_filtering_terms_of_genomicvariation(entry_id: Optional[str], qparams: RequestParams):
    query = {'scopes': 'genomicVariation'}
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
    query_parameters, parameters_as_filters = apply_request_parameters({}, qparams)
    LOG.debug(query_parameters)
    LOG.debug(parameters_as_filters)
    if parameters_as_filters == True:
        query, parameters_as_filters = apply_request_parameters({}, qparams)
        query_parameters={}
    else:
        query=query_parameters
    query = apply_filters(query, qparams.query.filters, collection,query_parameters)
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosampleId": 1, "_id": 0})
    biosample_id=biosample_ids["caseLevelData"]
    try:
        finalid=biosample_id[0]["biosampleId"]
    except Exception:
        finalid=biosample_id["biosampleId"]
    query = {"id": finalid}
    individual_id = client.beacon.biosamples \
        .find_one(query, {"individualId": 1, "_id": 0})
    finalid=individual_id["individualId"]
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
    return schema, count, dataset_count, docs, dataset