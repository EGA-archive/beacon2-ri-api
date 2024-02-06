import logging
from typing import Dict, List, Optional
from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.utils import query_id, query_ids, get_count, get_documents, get_cross_query, get_filtering_documents
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

                        
    if query_2 != {}:  
        return query_2
    else:
        return query


def get_individuals(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'individuals'
    query = apply_request_parameters({}, qparams)
    LOG.debug(qparams.query.filters)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.INDIVIDUALS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 100 or limit == 0:
        limit = 100
    if include == 'MISS':
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
                    if dataset_count !=0:
                        return schema, count, -1, None
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.individuals,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    elif include == 'NONE':
            count = get_count(client.beacon.individuals, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.individuals,
            query,
            qparams.query.pagination.skip*limit,
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
                    LOG.debug(limit)
                    docs = get_documents(
                        client.beacon.individuals,
                        query_count,
                        qparams.query.pagination.skip*limit,
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
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs


def get_individual_with_id(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'individuals'
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.INDIVIDUALS
    with open("/beacon/beacon/request/datasets.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    include = qparams.query.include_resultset_responses
    limit = qparams.query.pagination.limit
    if limit > 100 or limit == 0:
        limit = 100
    if include == 'MISS':
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
                    if dataset_count!=0:
                        return schema, count, -1, None
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        client.beacon.individuals,
                        query_count,
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    elif include == 'NONE':
            count = get_count(client.beacon.individuals, query)
            dataset_count=0
            docs = get_documents(
            client.beacon.individuals,
            query,
            qparams.query.pagination.skip*limit,
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
                        qparams.query.pagination.skip*limit,
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
                        qparams.query.pagination.skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    return schema, count, dataset_count, docs


def get_variants_of_individual(entry_id: Optional[str], qparams: RequestParams, dataset: str):
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
            client.beacon.individuals,
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


def get_biosamples_of_individual(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'biosamples'
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
                    if dataset_count!=0:
                        return schema, count, -1, None
                    LOG.debug(dataset_count)
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

def get_analyses_of_individual(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'individuals'
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
                    if dataset_count!=0:
                        return schema, count, -1, None
                    LOG.debug(dataset_count)
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
