from beacon.db import client
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id
from beacon.request.model import RequestParams


def get_analyses(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    return DefaultSchemas.ANALYSES, client.beacon.analyses \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_analysis_with_id(entry_id: str, qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    return DefaultSchemas.ANALYSES, client.beacon.analyses \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)


def get_variants_of_analysis(entry_id: str, qparams: RequestParams):
    query = {"caseLevelData.analysisId": entry_id}
    query = apply_filters({}, qparams.query.filters)
    return DefaultSchemas.GENOMICVARIATIONS, client.beacon.genomicVariations \
        .find(query) \
        .skip(qparams.query.pagination.skip) \
        .limit(qparams.query.pagination.limit)
