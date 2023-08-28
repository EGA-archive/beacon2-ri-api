import logging
from typing import Optional
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents, get_cross_query, get_filtering_documents
from beacon.request.model import RequestParams
from beacon.db import client

LOG = logging.getLogger(__name__)


def get_cohorts(entry_id: Optional[str], qparams: RequestParams):
    collection = 'cohorts'
    query = apply_filters({}, qparams.query.filters, collection)
    schema = DefaultSchemas.COHORTS
    count = get_count(client.beacon.cohorts, query)
    docs = get_documents(
        client.beacon.cohorts,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_cohort_with_id(entry_id: Optional[str], qparams: RequestParams):
    collection = 'cohorts'
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    schema = DefaultSchemas.COHORTS
    count = get_count(client.beacon.cohorts, query)
    docs = get_documents(
        client.beacon.cohorts,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_individuals_of_cohort(entry_id: Optional[str], qparams: RequestParams):
    collection = 'cohorts'
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    cohort_ids = client.beacon.cohorts \
        .find_one(query, {"ids.individualIds": 1, "_id": 0})
    cohort_ids=get_cross_query(cohort_ids['ids'],'individualIds','id')
    query = apply_filters(cohort_ids, qparams.query.filters, collection)

    schema = DefaultSchemas.INDIVIDUALS
    count = get_count(client.beacon.individuals, query)
    docs = get_documents(
        client.beacon.individuals,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_analyses_of_cohort(entry_id: Optional[str], qparams: RequestParams):
    collection = 'cohorts'
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    cohort_ids = client.beacon.cohorts \
        .find_one(query, {"ids.biosampleIds": 1, "_id": 0})
    cohort_ids=get_cross_query(cohort_ids['ids'],'biosampleIds','biosampleId')
    query = apply_filters(cohort_ids, qparams.query.filters, collection)

    schema = DefaultSchemas.ANALYSES
    count = get_count(client.beacon.analyses, query)
    docs = get_documents(
        client.beacon.analyses,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_variants_of_cohort(entry_id: Optional[str], qparams: RequestParams):
    collection = 'cohorts'
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    individual_ids = client.beacon.cohorts \
        .find_one(query, {"ids.individualIds": 1, "_id": 0})
    biosample_ids = client.beacon.cohorts \
        .find_one(query, {"ids.biosampleIds": 1, "_id": 0})
    #LOG.debug(individual_ids['ids'])
    individual_ids['ids']['individualIds']=individual_ids['ids']['individualIds']+biosample_ids['ids']['biosampleIds']
    
    individual_ids=get_cross_query(individual_ids['ids'],'individualIds','caseLevelData.biosampleId')
    query = apply_filters(individual_ids, qparams.query.filters, collection)
    schema = DefaultSchemas.GENOMICVARIATIONS
    count = get_count(client.beacon.genomicVariations, query)
    docs = get_documents(
        client.beacon.genomicVariations,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_runs_of_cohort(entry_id: Optional[str], qparams: RequestParams):
    collection = 'cohorts'
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    cohort_ids = client.beacon.cohorts \
        .find_one(query, {"ids.biosampleIds": 1, "_id": 0})
    cohort_ids=get_cross_query(cohort_ids['ids'],'biosampleIds','biosampleId')
    query = apply_filters(cohort_ids, qparams.query.filters, collection)

    schema = DefaultSchemas.RUNS
    count = get_count(client.beacon.runs, query)
    docs = get_documents(
        client.beacon.runs,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_biosamples_of_cohort(entry_id: Optional[str], qparams: RequestParams):
    collection = 'cohorts'
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.cohorts, query)
    cohort_ids = client.beacon.cohorts \
        .find_one(query, {"ids.biosampleIds": 1, "_id": 0})
    cohort_ids=get_cross_query(cohort_ids['ids'],'biosampleIds','id')
    query = apply_filters(cohort_ids, qparams.query.filters, collection)

    schema = DefaultSchemas.BIOSAMPLES
    count = get_count(client.beacon.biosamples, query)
    docs = get_documents(
        client.beacon.biosamples,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


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
        qparams.query.pagination.limit
    )
    return schema, count, docs
