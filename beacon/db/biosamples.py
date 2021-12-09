from beacon.db import client
from beacon.db.filters import *
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import *
from beacon.request.model import RequestParams


def get_biosamples(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    return DefaultSchemas.BIOSAMPLES, client.beacon.biosamples \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_biosample_with_id(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    return DefaultSchemas.BIOSAMPLES, client.beacon.biosamples \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_variants_of_biosample(entry_id: str, qparams: RequestParams):
    query = {"caseLevelData.biosampleId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    return DefaultSchemas.GENOMICVARIATIONS, client.beacon.genomicVariations \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_analyses_of_biosample(entry_id: str, qparams: RequestParams):
    query = {"biosampleId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    return DefaultSchemas.ANALYSES, client.beacon.analyses \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_runs_of_biosample(entry_id: str, qparams: RequestParams):
    query = {"biosampleId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    return DefaultSchemas.RUNS, client.beacon.runs \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)
