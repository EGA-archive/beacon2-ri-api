import logging
import yaml
from typing import Optional
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents, get_cross_query, get_filtering_documents
from beacon.request.model import RequestParams
from beacon.db import client

LOG = logging.getLogger(__name__)


def get_cohorts(entry_id: Optional[str], qparams: RequestParams):
    collection = 'cohorts'
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection)
    schema = DefaultSchemas.COHORTS
    count = get_count(client.beacon.cohorts, query)
    docs = get_documents(
        client.beacon.cohorts,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.skip*limit
    )
    return schema, count, docs


def get_cohort_with_id(entry_id: Optional[str], qparams: RequestParams):
    collection = 'cohorts'
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    schema = DefaultSchemas.COHORTS
    count = get_count(client.beacon.cohorts, query)
    docs = get_documents(
        client.beacon.cohorts,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.skip*limit
    )
    return schema, count, docs


def get_individuals_of_cohort(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'cohorts'
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    with open("/beacon/beacon/request/cohorts.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    cohort_ids=get_cross_query(datasets_dict[entry_id],'individualIds','id')
    query = apply_filters(cohort_ids, qparams.query.filters, collection)

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
                    LOG.debug(dataset_count)
                    if dataset_count!=0:
                        return schema, count, -1, None
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
            client.beacon.analyses,
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


def get_analyses_of_cohort(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'cohorts'
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    with open("/beacon/beacon/request/cohorts.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    cohort_ids=get_cross_query(datasets_dict[entry_id],'biosampleIds','id')
    query = apply_filters(cohort_ids, qparams.query.filters, collection)
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


def get_variants_of_cohort(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'cohorts'
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    with open("/beacon/beacon/request/cohorts.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    individual_ids=get_cross_query(datasets_dict[entry_id],'individualIds','caseLevelData.biosampleId')
    query = apply_filters(individual_ids, qparams.query.filters, collection)
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
            client.beacon.genomicVariations,
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

def get_runs_of_cohort(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'cohorts'
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    with open("/beacon/beacon/request/cohorts.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    cohort_ids=get_cross_query(datasets_dict[entry_id],'biosampleIds','biosampleId')
    query = apply_filters(cohort_ids, qparams.query.filters, collection)
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


def get_biosamples_of_cohort(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'cohorts'
    dataset_count=0
    limit = qparams.query.pagination.limit
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    with open("/beacon/beacon/request/cohorts.yml", 'r') as datasets_file:
        datasets_dict = yaml.safe_load(datasets_file)
    cohort_ids=get_cross_query(datasets_dict[entry_id],'biosampleIds','id')
    query = apply_filters(cohort_ids, qparams.query.filters, collection)

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


def get_filtering_terms_of_cohort(entry_id: Optional[str], qparams: RequestParams):
    query = {'scope': 'cohorts'}
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
