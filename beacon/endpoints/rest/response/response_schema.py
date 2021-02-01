import logging
from enum import IntEnum

from .... import conf
from ....validation.fields import SchemaField

LOG = logging.getLogger(__name__)

class BeaconEntity(IntEnum):
    BIOSAMPLE = 1
    INDIVIDUAL = 2
    VARIANT = 3


def build_beacon_response(proxy,
                          data,
                          num_total_results,
                          qparams_converted,
                          by_entity_type,
                          non_accessible_datasets,
                          func_response_type):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(proxy, qparams_converted, by_entity_type),
        'response': build_response(data, num_total_results, qparams_converted, non_accessible_datasets, func_response_type)
    }
    return beacon_response


def build_meta(proxy, qparams, by_entity_type):
    """"Builds the `meta` part of the response
    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """

    schemas = [s for s in get_schemas(proxy, qparams)]

    meta = {
        'beaconId': conf.beacon_id,
        'apiVersion': conf.api_version,
        'receivedRequest': build_received_request(qparams, schemas, by_entity_type),
        'returnedSchemas': schemas,
    }
    return meta


def get_schemas(proxy, qparams):
    for key in proxy.__keys__:
        field = proxy.__fields__[key]
        if isinstance(field, SchemaField):
            name = getattr(proxy.__names__, key)
            yield getattr(qparams, name)[0]


def build_received_request(qparams, schemas, by_entity_type):
    """"Fills the `receivedRequest` part with the request data"""

    request = {
        'meta': {
            'requestedSchemas' : schemas,
            'apiVersion' : qparams.apiVersion,
        },
        'query': build_received_query(qparams, by_entity_type),
    }

    return request


def build_received_query(qparams, by_entity_type):
    g_variant = build_g_variant_params(qparams, by_entity_type)
    individual = build_individual_params(qparams, by_entity_type)
    biosample = build_biosample_params(qparams, by_entity_type)
    datasets = build_datasets_params(qparams)
    pagination = build_pagination_params(qparams)

    query_part = {}
    if g_variant:
        query_part['g_variant'] = g_variant
    if individual:
        query_part['individual'] = individual
    if biosample:
        query_part['biosample'] = biosample
    if datasets:
        query_part['datasets'] = datasets
    if qparams.filters:
        query_part['filters'] = qparams.filters
    if pagination:
        query_part['pagination'] = pagination

    return query_part


def build_g_variant_params(qparams, by_entity_type):
    """Fills the `gVariant` part with the request data"""

    g_variant_params = {}
    if qparams.start:
        g_variant_params['start'] = qparams.start
    if qparams.end:
        g_variant_params['end'] = qparams.end
    if qparams.referenceBases:
        g_variant_params['referenceBases'] = qparams.referenceBases
    if qparams.alternateBases:
        g_variant_params['alternateBases'] = qparams.alternateBases
    if qparams.assemblyId:
        g_variant_params['assemblyId'] = qparams.assemblyId
    if qparams.referenceName:
        g_variant_params['referenceName'] = qparams.referenceName

    if by_entity_type == BeaconEntity.VARIANT and qparams.targetIdReq:
        g_variant_params['id'] = qparams.targetIdReq

    return g_variant_params


def build_individual_params(qparams, by_entity_type):
    """Fills the `individual` part with the request data"""

    individual_params = {}
    if by_entity_type == BeaconEntity.INDIVIDUAL and qparams.targetIdReq:
        individual_params['id'] = qparams.targetIdReq

    return individual_params


def build_biosample_params(qparams, by_entity_type):
    """Fills the `biosample` part with the request data"""

    biosample_params = {}
    if by_entity_type == BeaconEntity.BIOSAMPLE and qparams.targetIdReq:
        biosample_params['id'] = qparams.targetIdReq

    return biosample_params


def build_datasets_params(qparams):
    """Fills the `datasets` part with the request data"""

    datasets_params = {}
    if qparams.datasetIds:
        datasets_params['datasets'] = qparams.datasetIds

    if qparams.includeDatasetResponses:
        datasets_params['includeDatasetResponses'] = qparams.includeDatasetResponses

    return datasets_params


def build_pagination_params(qparams):
    pagination_params = {}
    if qparams.limit:
        pagination_params['limit'] = qparams.limit
    if qparams.skip:
        pagination_params['skip'] = qparams.skip

    return pagination_params


def build_error(non_accessible_datasets):
    """"
    Fills the `error` part in the response.
    This error only applies to partial errors which do not prevent the Beacon from answering.
    """

    message = f'You are not authorized to access some of the requested datasets: {non_accessible_datasets}'

    return {
        'error': {
            'errorCode': 401,
            'errorMessage': message
        }
    }


def build_response(data, num_total_results, qparams, non_accessible_datasets, func):
    """"Fills the `response` part with the correct format in `results`"""

    # LOG.debug('Calling f= %s', func)

    response = {
            'exists': bool(data),
            'numTotalResults': int(num_total_results[0]),
            'results': func(data, qparams),
            'info': None,
            'resultsHandover': None, # build_results_handover
            'beaconHandover': conf.beacon_handovers,
        }

    if non_accessible_datasets:
        response['error'] = build_error(non_accessible_datasets)

    return response


def build_variant_response(data, qparams):
    """"Fills the `results` part with the format for variant data"""

    variant_func = qparams.requestedSchema[1]
    variant_annotation_func = qparams.requestedAnnotationSchema[1]

    for row in data:
        yield {
            'variant': variant_func(row),
            'variantAnnotations': variant_annotation_func(row),
            'handovers': None,  # build_variant_handover
            'datasetAlleleResponses': row['dataset_response']
        }


def build_biosample_or_individual_response(data, qparams):
    """"Fills the `results` part with the format for biosample or individual data"""

    return [qparams.requestedSchema[1](row) for row in data]
