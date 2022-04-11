from typing import Optional
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents
from beacon.request.model import RequestParams
from beacon.db import client


def get_cohorts(entry_id: Optional[str], qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
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
    query = apply_filters({}, qparams.query.filters)
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
    # TODO
    pass


def get_filtering_terms_of_cohort(entry_id: Optional[str], qparams: RequestParams):
    # TODO
    pass
