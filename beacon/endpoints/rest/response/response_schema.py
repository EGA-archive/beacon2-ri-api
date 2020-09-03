import logging

import itertools

from .... import conf
from ..schemas import SUPPORTED_SCHEMAS, DEFAULT_SCHEMAS
from ....utils.json import jsonb

LOG = logging.getLogger(__name__)


def build_beacon_response(data, qparams_converted, func_response_type, variant_id=None, individual_id=None,
                          biosample_id=None,):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams_converted, func_response_type, variant_id, individual_id, biosample_id),
        'response': build_response(data, qparams_converted, func_response_type)
    }
    return beacon_response


def build_meta(qparams, func_response_type, variant_id=None, individual_id=None, biosample_id=None):
    """"Builds the `meta` part of the response

    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """

    meta = {
        'beaconId': conf.beacon_id,
        'apiVersion': conf.api_version,
        'receivedRequest': build_received_request(qparams, variant_id, individual_id, biosample_id),
        'returnedSchemas': build_returned_schemas(qparams, func_response_type)
    }
    return meta


def build_received_request(qparams, variant_id=None, individual_id=None, biosample_id=None):
    """"Fills the `receivedRequest` part with the request data"""

    request = {
        'meta': {
            'requestedSchemas' : build_requested_schemas(qparams),
            'apiVersion' : qparams.apiVersion,
        },
        'query': build_received_query(qparams, variant_id, individual_id, biosample_id),
    }

    return request


def build_received_query(qparams, variant_id=None, individual_id=None, biosample_id=None):
    g_variant = build_g_variant_params(qparams, variant_id)
    individual = build_individual_params(qparams, individual_id)
    biosample = build_biosample_params(qparams, biosample_id)
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


def build_g_variant_params(qparams, variant_id=None):
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

    if variant_id is not None:
        g_variant_params['id'] = variant_id

    return g_variant_params


def build_individual_params(qparams, individual_id=None):
    """Fills the `biosample` part with the request data"""

    individual_params = {}
    if individual_id is not None:
        individual_params['id'] = individual_id

    return individual_params


def build_biosample_params(qparams, biosample_id=None):
    """Fills the `inidividual` part with the request data"""

    biosample_params = {}
    if biosample_id is not None:
        biosample_params['id'] = biosample_id

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


def build_requested_schemas(qparams):
    """"
    Fills the `requestedSchemas` part with the request data
    It includes valid and invalid schemas requested by the user.
    """

    requested_schemas = {}

    if qparams.requestedSchemasVariant[0] or qparams.requestedSchemasVariant[1]:
        requested_schemas['Variant'] = [s for s, f in qparams.requestedSchemasVariant[0]] + list(
            qparams.requestedSchemasVariant[1])

    if qparams.requestedSchemasVariantAnnotation[0] or qparams.requestedSchemasVariantAnnotation[1]:
        requested_schemas['VariantAnnotation'] = [s for s, f in qparams.requestedSchemasVariantAnnotation[0]] + list(
            qparams.requestedSchemasVariantAnnotation[1])

    if qparams.requestedSchemasIndividual[0] or qparams.requestedSchemasIndividual[1]:
        requested_schemas['Individual'] = [s for s, f in qparams.requestedSchemasIndividual[0]] + list(
            qparams.requestedSchemasIndividual[1])

    if qparams.requestedSchemasBiosample[0] or qparams.requestedSchemasBiosample[1]:
        requested_schemas['Biosample'] = [s for s, f in qparams.requestedSchemasBiosample[0]] + list(
            qparams.requestedSchemasBiosample[1])

    return requested_schemas


def build_returned_schemas(qparams, func_response_type):
    """"
    Fills the `returnedSchema` part with the actual schemas returned in the response.
    This is the default schema for each type and any valid schema requested by the user.
    """

    # LOG.debug('func_response_type= %s', func_response_type.__name__)

    returned_schemas_by_response_type = {
        'build_variant_response': {
            'Variant': [DEFAULT_SCHEMAS['Variant']] if not qparams.requestedSchemasVariant[0] else []
                       + [s for s, f in qparams.requestedSchemasVariant[0]],
            'VariantAnnotation': [DEFAULT_SCHEMAS['VariantAnnotation']] if not qparams.requestedSchemasVariantAnnotation[0] else []
                                 + [s for s, f in qparams.requestedSchemasVariantAnnotation[0]],
        }, 'build_individual_response': {
            'Individual': [DEFAULT_SCHEMAS['Individual']] if not qparams.requestedSchemasIndividual[0] else []
                          + [s for s, f in qparams.requestedSchemasIndividual[0]],
        }, 'build_biosample_response': {
            'Biosample': [DEFAULT_SCHEMAS['Biosample']] if not qparams.requestedSchemasBiosample[0] else []
                         + [s for s, f in qparams.requestedSchemasBiosample[0]],
        },
    }

    return returned_schemas_by_response_type[func_response_type.__name__] # We let it throw a KeyError


def build_error(qparams):
    """"
    Fills the `error` part in the response.
    This error only applies to partial errors which do not prevent the Beacon from answering.
    """

    if not qparams.requestedSchemasVariant[1] and not qparams.requestedSchemasVariantAnnotation[1] \
            and not qparams.requestedSchemasIndividual[1] and not qparams.requestedSchemasBiosample[1]:
         # Do nothing
         return

    message = 'Some requested schemas are not supported.'

    if len(qparams.requestedSchemasVariant[1]) > 0:
        message += f' Variant: {qparams.requestedSchemasVariant[1]}'

    if len(qparams.requestedSchemasVariantAnnotation[1]) > 0:
        message += f' VariantAnnotation: {qparams.requestedSchemasVariantAnnotation[1]}'

    if len(qparams.requestedSchemasIndividual[1]) > 0:
        message += f' Individual: {qparams.requestedSchemasIndividual[1]}'

    if len(qparams.requestedSchemasBiosample[1]) > 0:
        message += f' Biosample: {qparams.requestedSchemasBiosample[1]}'

    return {
        'error': {
            'errorCode': 206,
            'errorMessage': message
        }
    }


def build_response(data, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""

    response = {
            'exists': len(data) > 0,
            'results': func(data, qparams),
            'info': None,
            'resultsHandover': None, # build_results_handover
            'beaconHandover': None, # build_beacon_handover
        }

    error = build_error(qparams)
    if error is not None:
        response['error'] = error

    return response


def build_variant_response(data, qparams):
    """"Fills the `results` part with the format for variant data"""

    variant_requested_schemas = qparams.requestedSchemasVariant[0]
    variant_annotation_requested_schemas = qparams.requestedSchemasVariantAnnotation[0]
    # LOG.debug('variant_requested_schemas= %s', variant_requested_schemas)
    # LOG.debug('variant_annotation_requested_schemas= %s', variant_annotation_requested_schemas)

    variants = get_formatted_content(data, 'Variant', (variant_requested_schemas or []))
    variant_annotations = get_formatted_content(data, 'VariantAnnotation', (variant_annotation_requested_schemas or []))

    for (v, v_a, row) in itertools.zip_longest(variants, variant_annotations, data):
        # LOG.debug('v= %s', v)
        yield {
            'variant': v,
            'variantAnnotations': v_a,
            'variantHandover': None,  # build_variant_handover
            'datasetAlleleResponses': jsonb(row['dataset_response'])
        }


def build_individual_response(data, qparams):
    """"Fills the `results` part with the format for individual data"""

    individual_requested_schemas = qparams.requestedSchemasIndividual[0]
    # LOG.debug('individual_requested_schemas= %s', individual_requested_schemas)

    return get_formatted_content(data, 'Individual', (individual_requested_schemas or []))


def build_biosample_response(data, qparams):
    """"Fills the `results` part with the format for sample data"""

    biosample_requested_schemas = qparams.requestedSchemasBiosample[0]
    # LOG.debug('biosample_requested_schemas= %s', biosample_requested_schemas)

    return get_formatted_content(data, 'Biosample', (biosample_requested_schemas or []))


def get_formatted_content(data, field_name, schemas):
    """Formats the data according to the first requested schema"""
    # LOG.debug('schemas: %s', schemas)

    if not schemas:
        default_schema = DEFAULT_SCHEMAS[field_name] # We let it throw a KeyError
        schemas = [(default_schema, SUPPORTED_SCHEMAS[default_schema])]

    schema, func = schemas.pop()
    return [func(row) for row in data]
