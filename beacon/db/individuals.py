from beacon.db import client
from beacon.db.filters import apply_filters
from beacon.db.utils import query_id
from beacon.request.model import RequestParams


def get_individuals(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    return client.beacon.individuals\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_individual_with_id(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    return client.beacon.individuals\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_variants_of_individual(entry_id: str, qparams: RequestParams):
    query = { "individualId": entry_id }
    query = apply_filters(query, qparams.query.filters)
    return client.beacon.g_variants\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_biosamples_of_individual(entry_id: str, qparams: RequestParams):
    query = { "individualId": entry_id }
    query = apply_filters(query, qparams.query.filters)
    return client.beacon.biosamples\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_filtering_terms_of_individual(entry_id: str, qparams: RequestParams):
    # TODO
    pass


def get_runs_of_individual(entry_id: str, qparams: RequestParams):
    # TODO: To be fixed in the model
    pass


def get_analyses_of_individual(entry_id: str, qparams: RequestParams):
    # TODO: To be fixed in the model
    pass
