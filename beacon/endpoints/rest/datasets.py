import logging

from ...utils import resolve_token
from ...validation.request import RequestParameters, print_qparams
from ...validation.fields import SchemasField, RegexField
from ...utils.db import fetch_datasets_metadata
from ...utils.stream import json_stream
from .response.info_response_schema import build_beacon_response, build_dataset_info_response


LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class DatasetParameters(RequestParameters):
    # requested schemas
    requestedSchemasServiceInfo = SchemasField()
    requestedSchemasDataset = SchemasField()
    apiVersion = RegexField(r'^v[0-9]+(\.[0-9]+)*$')


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

proxy_info = DatasetParameters()


async def handler(request):
    LOG.info('Running a GET datasets request')
    _, qparams_db = await proxy_info.fetch(request)

    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy_info, LOG)

    # Fetch datasets info
    beacon_datasets = [r async for r in fetch_datasets_metadata()]

    all_datasets = [r['datasetId'] for r in beacon_datasets]

    access_token = request.headers.get('Authorization')
    if access_token:
        access_token = access_token[7:] # cut out 7 characters: len('Bearer ')

    authorized_datasets, authenticated = await resolve_token(access_token, all_datasets)
    if authenticated:
        LOG.debug('all datasets:  %s', all_datasets)
        LOG.info('resolved datasets:  %s', authorized_datasets)

    response_converted = build_beacon_response(beacon_datasets,
                                               qparams_db,
                                               build_dataset_info_response,
                                               authorized_datasets if authenticated else [])
    return await json_stream(request, response_converted)
