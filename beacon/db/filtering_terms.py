from typing import Optional
from beacon.db import client
from beacon.db.filters import apply_filters
from beacon.db.utils import query_id, get_documents, get_count, get_filtering_documents
from beacon.request.model import RequestParams
from beacon.db.schemas import DefaultSchemas

def get_filtering_terms(entry_id: Optional[str], qparams: RequestParams):
    query = {}
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


def get_filtering_term_with_id(entry_id: Optional[str], qparams: RequestParams):
    collection = 'filtering_terms'
    query = apply_filters({}, qparams.query.filters, collection)
    query = query_id(query, entry_id)
    schema = None
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
