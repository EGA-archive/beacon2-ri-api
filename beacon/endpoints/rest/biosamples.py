import logging

from aiohttp import web

from ...utils import resolve_token
from ...utils.stream import json_stream
from ...utils.db import fetch_variants, fetch_biosamples, fetch_individuals
from ...validation.request import print_qparams
from ...validation.fields import SchemaField
from .response.response_schema import (build_beacon_response,
                                       build_variant_response,
                                       build_biosample_or_individual_response)
from . import GVariantParametersBase

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

class BiosamplesParameters(GVariantParametersBase):
    requestedSchema = SchemaField('ga4gh-phenopacket-biosample-v1.0',
                                  'beacon-biosample-v2.0.0-draft.2',
                                  default='beacon-biosample-v2.0.0-draft.2')

class IndividualsParameters(GVariantParametersBase):
    requestedSchema = SchemaField('ga4gh-phenopacket-individual-v1.0',
                                  'beacon-individual-v2.0.0-draft.2',
                                  default='beacon-individual-v2.0.0-draft.2')

class GVariantsParameters(GVariantParametersBase):
    requestedSchema = SchemaField('beacon-variant-v2.0.0-draft.2',
                                  'ga4gh-phenopacket-variant-v1.0',
                                  default='beacon-variant-v2.0.0-draft.2')
    requestedAnnotationSchema = SchemaField('beacon-variant-annotation-v2.0.0-draft.2',
                                            'ga4gh-phenopacket-variant-annotation-v1.0',
                                  default='beacon-variant-annotation-v2.0.0-draft.2')

biosamples_proxy = BiosamplesParameters()
gvariants_proxy = GVariantsParameters()
individuals_proxy = IndividualsParameters()

def generic_handler(proxy, fetch_func, func_response_type):
    def decorator(func):
        async def wrapper(request):
            LOG.info('Running a request for %s', func)
            _, qparams_db = await proxy.fetch(request)
            if LOG.isEnabledFor(logging.DEBUG):
                print_qparams(qparams_db, proxy, LOG)

            access_token = request.headers.get('Authorization')
            if access_token:
                access_token = access_token[7:] # cut out 7 characters: len('Bearer ')

            datasets, authenticated = await resolve_token(access_token, qparams_db.datasetIds)
            non_accessible_datasets = qparams_db.datasetIds - set(datasets)

            LOG.debug('requested datasets:  %s', qparams_db.datasetIds)
            LOG.debug('non_accessible_datasets: %s', non_accessible_datasets)
            LOG.debug('resolved datasets:  %s', datasets)

            if not datasets and non_accessible_datasets:
                error = f'You are not authorized to access any of these datasets: {non_accessible_datasets}'
                raise web.HTTPUnauthorized(reason=error)

            response = fetch_func(qparams_db, datasets, authenticated, biosample_stable_id=qparams_db.targetIdReq)
            rows = [row async for row in response]
            # build_beacon_response knows how to loop through it
            response_converted = build_beacon_response(rows,
                                                       qparams_db,
                                                       non_accessible_datasets,
                                                       func_response_type,
                                                       biosample_id=qparams_db.targetIdReq)

            return await func(request, response_converted, non_accessible_datasets)
        return wrapper
    return decorator

@generic_handler(individuals_proxy, fetch_individuals, build_biosample_or_individual_response)
async def handler_individuals(request, response_converted, non_accessible_datasets):
    LOG.info('Formatting the response for the individuals')
    return await json_stream(request, response_converted, partial=bool(non_accessible_datasets))


@generic_handler(biosamples_proxy, fetch_biosamples, build_biosample_or_individual_response)
async def handler_biosamples(request, response_converted, non_accessible_datasets):
    LOG.info('Formatting the response for the biosamples')

    return await json_stream(request, response_converted, partial=bool(non_accessible_datasets))


@generic_handler(gvariants_proxy, fetch_variants, build_variant_response)
async def handler_gvariants(request, response_converted, non_accessible_datasets):
    LOG.info('Formatting the response for the variants')

    return await json_stream(request, response_converted, partial=bool(non_accessible_datasets))
