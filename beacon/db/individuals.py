from beacon.db import client
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id
from beacon.request.model import RequestParams
import json
from bson import json_util


def get_individuals(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    return DefaultSchemas.INDIVIDUALS, client.beacon.individuals \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_individual_with_id(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    return DefaultSchemas.INDIVIDUALS, client.beacon.individuals \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_variants_of_individual(entry_id: str, qparams: RequestParams):
    query = {"individualId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    return DefaultSchemas.GENOMICVARIATIONS, client.beacon.genomicVariations \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_biosamples_of_individual(entry_id: str, qparams: RequestParams):
    query = {"individualId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    return DefaultSchemas.BIOSAMPLES, client.beacon.biosamples \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_filtering_terms_of_individual(entry_id: str, qparams: RequestParams):
    # TODO
    pass


def get_runs_of_individual(entry_id: str, qparams: RequestParams):
    query = {"caseLevelData.individualId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    run_ids = client.beacon.genomicVariations.find_one(query, {"caseLevelData.runId": 1, "_id": 0})
    run_ids = [json.loads(json_util.dumps(r)) for r in run_ids] if run_ids else []

    query = query_id({}, run_ids)
    query = apply_filters(query, qparams.query.filters)
    return DefaultSchemas.RUNS, client.beacon.runs \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_analyses_of_individual(entry_id: str, qparams: RequestParams):
    query = {"caseLevelData.individualId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    analysis_ids = client.beacon.genomicVariations.find_one(query, {"caseLevelData.analysisId": 1, "_id": 0})
    analysis_ids = [json.loads(json_util.dumps(r)) for r in analysis_ids] if analysis_ids else []

    query = query_id({}, analysis_ids)
    query = apply_filters(query, qparams.query.filters)
    return DefaultSchemas.ANALYSES, client.beacon.analyses \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)
