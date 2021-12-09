from beacon.db.filters import apply_alphanumeric_filter, apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, query_ids
from beacon.request.model import AlphanumericFilter, RequestParams
from beacon.db import client

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
    return DefaultSchemas.GENOMICVARIATIONS, client.beacon.genomicVariations \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_variant_with_id(entry_id: str, qparams: RequestParams):
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters)
    query = query_id(query, entry_id)
    return DefaultSchemas.GENOMICVARIATIONS, client.beacon.genomicVariations \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_biosamples_of_variant(entry_id: str, qparams: RequestParams):
    query = apply_request_parameters({}, qparams)
    query = apply_filters(query, qparams.query.filters)
    query = query_id(query, entry_id)
    ids = client.beacon.genomicVariations \
        .find_one(query, {"biosamplesIds": 1})

    query = apply_request_parameters({}, qparams)
    query = query_ids(query, ids)
    return DefaultSchemas.BIOSAMPLES, client.beacon.biosamples \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_individuals_of_variant(entry_id: str, qparams: RequestParams):
    query = {"variantIds": entry_id}
    query = apply_request_parameters(query, qparams)
    return DefaultSchemas.INDIVIDUALS, client.beacon.individuals \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_runs_of_variant(entry_id: str, qparams: RequestParams):
    # TODO: To be fixed in the model
    pass


def get_analyses_of_variant(entry_id: str, qparams: RequestParams):
    # TODO: To be fixed in the model
    pass
