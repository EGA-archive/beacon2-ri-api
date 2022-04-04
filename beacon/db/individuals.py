from typing import Optional
from beacon.db import client
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents
from beacon.request.model import RequestParams
import json
from bson import json_util


def get_individuals(entry_id: Optional[str], qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    schema = DefaultSchemas.INDIVIDUALS
    count = get_count(client.beacon.individuals, query)
    docs = get_documents(
        client.beacon.individuals,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_individual_with_id(entry_id: Optional[str], qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    schema = DefaultSchemas.INDIVIDUALS
    count = get_count(client.beacon.individuals, query)
    docs = get_documents(
        client.beacon.individuals,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_variants_of_individual(entry_id: Optional[str], qparams: RequestParams):
    query = {"individualId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    schema = DefaultSchemas.GENOMICVARIATIONS
    count = get_count(client.beacon.genomicVariations, query)
    docs = get_documents(
        client.beacon.genomicVariations,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_biosamples_of_individual(entry_id: Optional[str], qparams: RequestParams):
    query = {"individualId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    schema = DefaultSchemas.BIOSAMPLES
    count = get_count(client.beacon.biosamples, query)
    docs = get_documents(
        client.beacon.biosamples,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_filtering_terms_of_individual(entry_id: Optional[str], qparams: RequestParams):
    # TODO
    pass


def get_runs_of_individual(entry_id: Optional[str], qparams: RequestParams):
    query = {"caseLevelData.individualId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    run_ids = client.beacon.genomicVariations.find_one(query, {"caseLevelData.runId": 1, "_id": 0})
    run_ids = [json.loads(json_util.dumps(r)) for r in run_ids] if run_ids else []

    query = query_id({}, run_ids)
    query = apply_filters(query, qparams.query.filters)

    schema = DefaultSchemas.RUNS
    count = get_count(client.beacon.runs, query)
    docs = get_documents(
        client.beacon.runs,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_analyses_of_individual(entry_id: Optional[str], qparams: RequestParams):
    query = {"caseLevelData.individualId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    analysis_ids = client.beacon.genomicVariations.find_one(query, {"caseLevelData.analysisId": 1, "_id": 0})
    analysis_ids = [json.loads(json_util.dumps(r)) for r in analysis_ids] if analysis_ids else []

    query = query_id({}, analysis_ids)
    query = apply_filters(query, qparams.query.filters)

    schema = DefaultSchemas.ANALYSES
    count = get_count(client.beacon.analyses, query)
    docs = get_documents(
        client.beacon.analyses,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs
