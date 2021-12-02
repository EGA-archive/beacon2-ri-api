from beacon.db import client
from beacon.db.filters import apply_filters
from beacon.db.utils import query_id
from beacon.request.model import RequestParams


def get_filtering_terms(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    return None, client.beacon.filtering_terms\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_filtering_term_with_id(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    return None, client.beacon.filtering_terms\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)
