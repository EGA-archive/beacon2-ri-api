from beacon.db.filters import apply_filters
from beacon.db.utils import query_id, query_ids
from beacon.request.model import RequestParams
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

def get_variants(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    return client.beacon.g_variants\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_variant_with_id(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    return client.beacon.g_variants\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_biosamples_of_variant(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    ids = client.beacon.g_variants\
        .find_one(query, { "biosamplesIds": 1 })
    
    query = query_ids({}, ids)
    return client.beacon.biosamples\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_individuals_of_variant(entry_id: str, qparams: RequestParams):
    query = { "variantIds": entry_id }
    return client.beacon.individuals\
        .find(query)\
        .skip(qparams.query.pagination.skip)\
        .limit(qparams.query.pagination.limit)


def get_runs_of_variant(entry_id: str, qparams: RequestParams):
    # TODO: To be fixed in the model
    pass


def get_analyses_of_variant(entry_id: str, qparams: RequestParams):
    # TODO: To be fixed in the model
    pass
