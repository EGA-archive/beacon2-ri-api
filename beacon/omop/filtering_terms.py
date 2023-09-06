from typing import Optional
from beacon.omop import client
from beacon.omop.filters import apply_filters
from beacon.omop.utils import query_id, get_documents, get_count, get_filtering_documents
from beacon.request.model import RequestParams
from beacon.omop.schemas import DefaultSchemas
from beacon.omop.individuals import get_filtering_terms_of_individual
from beacon.omop.biosamples import get_filtering_terms_of_biosample


def get_filtering_terms(entry_id: Optional[str], qparams: RequestParams):
    schema = None
    schemaInd, indCount, indDocs = get_filtering_terms_of_individual(None, None)
    schemaInd, bioCount, bioDocs = get_filtering_terms_of_biosample(None, None)

    return schema, indCount + bioCount, indDocs + bioDocs



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
