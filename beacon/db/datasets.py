from beacon.db.filters import apply_filters
from beacon.db.utils import query_id
from beacon.request.model import RequestParams
from beacon.db import client

import logging
import json
LOG = logging.getLogger(__name__)

def get_datasets(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    return client.beacon.datasets\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_dataset_with_id(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    return client.beacon.datasets\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_variants_of_dataset(entry_id: str, qparams: RequestParams):
    query = { "datasetId": entry_id }
    query = apply_filters(query, qparams.query.filters)
    return client.beacon.g_variants\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_biosamples_of_dataset(entry_id: str, qparams: RequestParams):
    query = { "datasetId": entry_id }
    query = apply_filters(query, qparams.query.filters)
    return client.beacon.biosamples\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_individuals_of_dataset(entry_id: str, qparams: RequestParams):
    query = { "datasetId": entry_id }
    query = apply_filters(query, qparams.query.filters)
    return client.beacon.individuals\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def filter_public_datasets(requested_datasets_ids):
    query = { "dataUseConditions.duoDataUse.modifiers.id" : "DUO:0000004" }
    return client.beacon.datasets\
        .find(query)


def get_filtering_terms_of_dataset(entry_id: str, qparams: RequestParams):
    # TODO
    pass


def get_runs_of_dataset(entry_id: str, qparams: RequestParams):
    # TODO: To be fixed in the model
    pass


def get_analyses_of_dataset(entry_id: str, qparams: RequestParams):
    # TODO: To be fixed in the model
    pass
