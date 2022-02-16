from beacon.db import client
from beacon.db.filters import apply_filters
from beacon.db.utils import query_id, get_documents, get_count
from beacon.request.model import RequestParams


def get_filtering_terms(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    schema = None
    count = get_count(client.beacon.filtering_terms, query)
    docs = get_documents(
        client.beacon.filtering_terms,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_filtering_term_with_id(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    schema = None
    count = get_count(client.beacon.filtering_terms, query)
    docs = get_documents(
        client.beacon.filtering_terms,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs
