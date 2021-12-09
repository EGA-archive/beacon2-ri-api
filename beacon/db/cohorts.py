from pymongo.message import _SKIPLIM
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id
from beacon.request.model import RequestParams
from beacon.db import client


def get_cohorts(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    return DefaultSchemas.COHORTS, client.beacon.cohorts\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_cohort_with_id(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    return DefaultSchemas.COHORTS, client.beacon.cohorts\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_individuals_of_cohort(entry_id: str, qparams: RequestParams):
    # TODO
    pass


def get_filtering_terms_of_cohort(entry_id: str, qparams: RequestParams):
    # TODO
    pass
