"""
Samples/Individuals Endpoint.

* ``/samples/{sample_id}`` 
* ``/individuals/{individual_id}`` 

Query samples/individuals by ID. 
"""
import ast
import logging
import requests
import random
import pandas as pd

from .exceptions import BeaconBadRequest, BeaconServerError, BeaconForbidden, BeaconUnauthorised
from .. import __apiVersion__, __id__
from ..conf.config import DB_SCHEMA

from ..utils.polyvalent_functions import create_prepstmt_variables, filter_exists, datasetHandover
from ..utils.polyvalent_functions import prepare_filter_parameter, parse_filters_request
from ..utils.polyvalent_functions import fetch_datasets_access, access_resolution
from ..utils.models import variant_object, variantAnnotation_object, biosample_object, individual_object

from .genomic_query import fetch_resulting_datasets, fetch_variantAnnotations, snp_resultsHandover
from .samples_ind import get_results_simple

LOG = logging.getLogger(__name__)





# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

#######################
#######  BY ID ########
#######################

async def by_id_handler(db_pool, request, processed_request):
    # First we are going to get the lists of the available datasets
    public_datasets, registered_datasets, controlled_datasets = await fetch_datasets_access(db_pool, '')

        ##### TEST
        # access_type, accessible_datasets = access_resolution(request, request['token'], request.host, public_datasets, registered_datasets, controlled_datasets)
        # LOG.info(f"The user has this types of access: {access_type}")
        # query_parameters[-2] = ",".join([str(id) for id in accessible_datasets])
        ##### END TEST

    # NOTICE that right now we will just focus on the PUBLIC ones to ease the process, so we get all their ids and add them to the query
    valid_datasets = public_datasets

    # Do the actual query
    target_id_req = request.match_info['target_id_req']
    results = await get_results_simple(db_pool, valid_datasets, request, processed_request, target_id_req = target_id_req)

    return results
