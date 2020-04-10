"""
Individuals Endpoint.

* ``/individuals`` 

Query individuals, use variant/samples/individuals filters. 
"""
import logging
import pandas as pd
import sys


from ..utils.polyvalent_functions import fetch_datasets_access, access_resolution
from ..utils.models import individual_object_rest


from .exceptions import BeaconBadRequest, BeaconServerError, BeaconForbidden, BeaconUnauthorised
from .. import __apiVersion__, __id__
from ..conf.config import DB_SCHEMA
from ..utils import capture_server_error


# Constants

## Logs
LOG = logging.getLogger(__name__)

## Make lists with the column names that the main SQL function returns
individual_columns = ['individual_stable_id', 'sex', 'ethnicity', 'geographic_origin']
disease_columns = ['disease_id', 'disease_age_of_onset_age', 'disease_age_of_onset_age_group', 'disease_stage', 'disease_family_history']
pedigree_columns = ['pedigree_stable_id', 'pedigree_role', 'pedigree_no_individuals_tested', 'pedigree_disease_id']         


# ----------------------------------------------------------------------------------------------------------------------
#                                         SECONDARY FUNCTIONS (called by the main functions)
# ----------------------------------------------------------------------------------------------------------------------

def create_query(processed_request):
    """
    Restructure the request to build the query object
    """

    return {
        "variant": {
            "referenceBases": processed_request.get("referenceBases", ""),
            "alternateBases": processed_request.get("alternateBases", ""),
            "referenceName": processed_request.get("referenceName", ""),
            "start": processed_request.get("start"),
            "end": processed_request.get("end"),
            "assemblyId": processed_request.get("assemblyId", "")
            },
        "datasets": {
            "datasetIds": processed_request.get("datasetIds"),
            "includeDatasetResponses": ""
             },
        "filters": processed_request.get("filters"),
    }

def simple_listener(c, m):
    """We pass this to connection.add_log_listener() 
    for getting the SQL Messages in the LOGS of the Beacon.
    """
    LOG.debug(m)  # We ignore "c"


# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN FUNCTIONS (called by the handler)
# ----------------------------------------------------------------------------------------------------------------------

def create_final_response(raw_request, results, alternative_schemas):
    """
    Create the final response as the Beacon Schema expects. 
    """
    alt_schemas_ind = alternative_schemas
    query = create_query(raw_request)

    final_response = {
        "meta": {
            "beaconId": __id__,
            "apiVersion": __apiVersion__,
            "receivedRequest": {
                "meta": {
                    "requestedSchemas": {
                        "individualSchemas": alt_schemas_ind
                        # REVIEW
                    },
                    "apiVersion": __apiVersion__  # it is hardcoded because we only return v2 for this endpoint
                },
                "query": query
            },
            "returnedSchemas": {
                "Individual": ["beacon-individual-v0.1"] + alt_schemas_ind
            }
        },
        "value": {
            "exists": any(results),
            "error": None,
            "results": results,
            "info": {},
            "resultsHandover": [],
            "beaconHandover": [ { "handoverType" : {
                                                "id" : "CUSTOM",
                                                "label" : "Organization contact"
                                                },
                                                "note" : "Organization contact details maintaining this Beacon",
                                                "url" : "mailto:beacon.ega@crg.eu"
                                            } ]
        }
    }

    return final_response

def create_individuals_object(response_df, schemas_request):
    """
    Shapes the individuals DataFrame response into a Beacon object.
    Takes the request to check if alternativeSchemas have been requested.
    """
    # Here we use the lists with the column names that the main SQL function returns

    responses_list = []
    by_individual = response_df.groupby('individual_stable_id')
    for _, individual_df in by_individual:
        individual = individual_df[individual_columns].drop_duplicates().to_dict('r')[0]
        # adding the info about diseases and pedigrees
        diseases = individual_df[disease_columns].drop_duplicates().to_dict('r')
        individual['diseases'] = diseases
        pedigrees = individual_df[pedigree_columns].drop_duplicates().to_dict('r')
        individual['pedigrees'] = pedigrees

        responses_list.append(individual_object_rest(individual, schemas_request))
    
    return responses_list


@capture_server_error(prefix='Query individuals DB error: ')
async def get_result(db_pool, query_parameters):
    """
    Contacts the DB to fetch the info.
    Returns a pd.DataFrame with the response. 
    """

    async with db_pool.acquire(timeout=180) as connection:

        # connection.add_log_listener(simple_listener)
        dollars = ", ".join(["$" + str(i) for i in range(1, len(query_parameters) + 1)])
        query = f"""SELECT * FROM {DB_SCHEMA}.query_patients({dollars});"""
        LOG.debug("QUERY to fetch hits: %s", query)
        statement = await connection.prepare(query)
        db_response = await statement.fetch(*query_parameters)

        if db_response: # maybe better to test db_response
            # Converting the response to a DataFrame 
            response = [dict(record) for record in db_response]
            response_df = pd.DataFrame(response)
            # Making sure we don't have NaN values
            response_df = response_df.where(response_df.notnull(), None)
            return True, response_df
        else:
            LOG.debug("No response for this query.")
            return False, []

## We create a list of the parameters that the SQL function needs
_CORRECT_PARAMETERS =  [
    "variantType",  # _variant_type text
    "start",  # _start integer
    "startMin",  # _start_min integer
    "startMax",  # _start_max integer
    "end",  # _end integer
    "endMin",  # _end_min integer
    "endMax",  # _end_max integer
    "referenceName",  # _chromosome character varying
    "referenceBases",  # _reference_bases text
    "alternateBases",  # _alternate_bases text
    "assemblyId",  # _reference_genome text
    "datasetIds",  # _dataset_ids text
    "biosampleId", # _biosample_stable_id text,
    "individualId",  # _individual_stable_id text
    "filters", # _filters text
    "skip",  # _skip integer
    "limit"]  # _limit integer
_INT_PARAMS = ['start', 'end', 'endMax', 'endMin', 'startMax', 'startMin', 'skip', 'limit']
_LIST_PARAMETERS = ['datasetIds', 'filters', 'individualSchemas']

def request2queryparameters(raw_request):
    """
    Reorganize the request to match the query_patients() SQL function input.
    """

    ## Iterate correct_parameters to create the query_parameters list from the raw_request 
    ## in the required order and with the right types
    for param in _CORRECT_PARAMETERS:
        query_param = raw_request.get(param)
        if not (query_param or (isinstance(query_param,int) and query_param == 0)):  # control if the user has used the parameter
            yield None
            continue

        if param in _INT_PARAMS:
            yield query_param  # let it crash if not already an int
            continue
        if param in _LIST_PARAMETERS:
            yield ",".join(query_param)
            continue
        # otherwise
        yield query_param


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def get_individuals_rest(db_pool, request, processed_request):
    """
    Main function of the endpoint. 
    """

    # 1. GET VALID/ACCESSIBLE DATASETS

    datasets_request = processed_request.get("datasetIds")

    # We want to get a list of the datasets available in the database separated in three lists
    # depending on the access level (we check all of them if the user hasn't specified anything, if some
    # there were given, those are the only ones that are checked)
    public_datasets, registered_datasets, controlled_datasets = await fetch_datasets_access(db_pool, datasets_request)

    ##### TEST CODE TO USE WHEN AAI is integrated
    # access_type, accessible_datasets = access_resolution(request, request['token'], request.host, public_datasets,
    #                                                      registered_datasets, controlled_datasets)
    # LOG.info(f"The user has this types of access: {access_type}")
    # query_parameters[-2] = ",".join([str(id) for id in accessible_datasets])
    ##### END TEST

    # NOTE that right now we will just focus on the PUBLIC ones to ease the process, so we get all their 
    # ids and add them to the query
    datasets_request = ",".join(public_datasets)

    # 2. REQUEST PROCESSING

    # Add individualId parameter if used
    if dict(request.match_info):
        individual_id = request.match_info['target_id_req']
        processed_request.update({"individualId": individual_id})

    # Parse the request to prepare it to be used in the SQL function
    processed_request_upd = processed_request.copy()
    processed_request_upd["datasetIds"] = list(datasets_request)
    query_parameters = list(request2queryparameters(processed_request_upd))

    LOG.info("Query FINAL param: %s", query_parameters)

    # 3. RETRIEVE DATA FROM THE DB (use SQL function)
    LOG.info('Connecting to the DB to make the query.')
    exists, response_df = await get_result(db_pool, query_parameters)
    LOG.info('Query done.')
    
    # 4. CREATE INDIVIDUALS OBJECT
    LOG.info('Shaping the DB response.')

    # Also check request to see if there is any alternativeSchema
    alternative_schemas_req = processed_request.get("individualSchemas")
    alternative_schemas = alternative_schemas_req if alternative_schemas_req else []

    if exists:
        results = create_individuals_object(response_df, alternative_schemas)
    else:
        results = response_df
    LOG.info('Arrangement done.')

    # 5. CREATE FINAL RESPONSE
    LOG.info('Creating the final response.')
    final_response = create_final_response(processed_request, results, alternative_schemas)
    LOG.info('Done.')
    return final_response
