from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, query_ids, get_count, get_documents
from beacon.request.model import AlphanumericFilter, RequestParams
from beacon.db import client
import json
from bson import json_util


VARIANTS_PROPERTY_MAP = {
    "assemblyId": "position.assemblyId",
    "referenceName": "position.refseqId",
    "start": "position.start",
    "end": "position.end",
    "referenceBases": "referenceBases",
    "alternateBases": "alternateBases",
    "variantType": "variantType",
    "variantMinLength": None,
    "variantMaxLength": None,
    "mateName": None,
    "gene": "molecularAttributes.geneIds",
    "aachange": "molecularAttributes.aminoacidChanges"
}


def apply_request_parameters(query: dict, qparams: RequestParams):
    for k, v in qparams.query.request_parameters.items():
        query = apply_alphanumeric_filter(query, AlphanumericFilter(
            id=VARIANTS_PROPERTY_MAP[k],
            value=v
        ))
    return query


def get_variants(entry_id: str, qparams: RequestParams):
    query = apply_request_parameters({}, qparams)
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


def get_variant_with_id(entry_id: str, qparams: RequestParams):
    query = {"variantInternalId": entry_id}
    query = apply_request_parameters(query, qparams)
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


def get_biosamples_of_variant(entry_id: str, qparams: RequestParams):
    query = {"variantInternalId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters)
    biosample_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.biosamplesId": 1, "_id": 0})
    biosample_ids = [json.loads(json_util.dumps(r)) for r in biosample_ids] if biosample_ids else []

    query = apply_request_parameters({}, qparams)
    query = query_ids(query, biosample_ids)
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


def get_individuals_of_variant(entry_id: str, qparams: RequestParams):
    query = {"variantInternalId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters)
    individual_ids = client.beacon.genomicVariations \
        .find(query)
    individual_ids = [json.loads(json_util.dumps(r))["caseLevelData"]["individualId"] for r in individual_ids] if individual_ids else []

    query = apply_request_parameters({}, qparams)
    query = query_ids(query, individual_ids)
    query = apply_filters(query, qparams.query.filters)

    schema = DefaultSchemas.INDIVIDUALS
    count = get_count(client.beacon.individuals, query)
    docs = get_documents(
        client.beacon.individuals,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_runs_of_variant(entry_id: str, qparams: RequestParams):
    query = {"variantInternalId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters)
    run_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.runId": 1, "_id": 0})
    run_ids = [json.loads(json_util.dumps(r)) for r in run_ids] if run_ids else []

    query = apply_request_parameters({}, qparams)
    query = query_ids(query, run_ids)
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


def get_analyses_of_variant(entry_id: str, qparams: RequestParams):
    query = {"variantInternalId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters)
    analysis_ids = client.beacon.genomicVariations \
        .find_one(query, {"caseLevelData.analysisId": 1, "_id": 0})
    analysis_ids = [json.loads(json_util.dumps(r)) for r in analysis_ids] if analysis_ids else []

    query = apply_request_parameters({}, qparams)
    query = query_ids(query, analysis_ids)
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
