import logging
import yaml
from typing import Optional
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents, get_cross_query, get_filtering_documents, get_docs_by_response_type
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
    mongo_collection = client.beacon.individuals
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
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    idq="id"
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs


def get_analyses_of_cohort(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'cohorts'
    mongo_collection = client.beacon.analyses
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
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    idq="biosampleId"
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs


def get_variants_of_cohort(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'cohorts'
    mongo_collection = client.beacon.genomicVariations
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
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    idq="caseLevelData.biosampleId"
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs

def get_runs_of_cohort(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'cohorts'
    mongo_collection = client.beacon.runs
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
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    idq="biosampleId"
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
    return schema, count, dataset_count, docs


def get_biosamples_of_cohort(entry_id: Optional[str], qparams: RequestParams, dataset: str):
    collection = 'cohorts'
    mongo_collection = client.beacon.biosamples
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
    skip = qparams.query.pagination.skip
    if limit > 100 or limit == 0:
        limit = 100
    idq="id"
    count, dataset_count, docs = get_docs_by_response_type(include, query, datasets_dict, dataset, limit, skip, mongo_collection, idq)
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
