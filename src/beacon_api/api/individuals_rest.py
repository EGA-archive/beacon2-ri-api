"""
Individuals Endpoint.

* ``/individuals`` 

Query individuals, use variant/samples/individuals filters. 
"""
import logging
import pandas as pd


from ..utils.polyvalent_functions import fetch_datasets_access, access_resolution
from ..utils.polyvalent_functions import create_prepstmt_variables
from ..utils.models import individual_object_rest


from .exceptions import BeaconBadRequest, BeaconServerError, BeaconForbidden, BeaconUnauthorised
from .. import __apiVersion__, __id__
from ..conf.config import DB_SCHEMA


# Constants
LOG = logging.getLogger(__name__)
# Make lists with the column names that the main SQL function returns
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

    query = {
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
            # "includeDatasetResponses": "ALL" if not processed_request.get("includeDatasetResponses") else processed_request.get("includeDatasetResponses")
             },
        "filters": processed_request.get("filters"),
    }

    return query


# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN FUNCTIONS (called by the handler)
# ----------------------------------------------------------------------------------------------------------------------

def create_final_response(raw_request, results):
    """
    Create the final response as the Beacon Schema expects. 
    """
    alt_schemas_ind_req = raw_request.get("individualSchemas")
    alt_schemas_ind = [] if not alt_schemas_ind_req else alt_schemas_ind_req.split(",")
    query = create_query(raw_request)

    final_response = {
        "meta": {
            "beaconId": __id__,
            "apiVersion": __apiVersion__,
            "receivedRequest": {
                "meta": {
                    "requestedSchemas": {
                        "Individual": alt_schemas_ind
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
        individual.update({'diseases': diseases})
        pedigrees = individual_df[pedigree_columns].drop_duplicates().to_dict('r')
        individual.update({'pedigrees': pedigrees})

        responses_list.append(individual_object_rest(individual, schemas_request))
    
    return responses_list


async def get_result(db_pool, query_parameters):
    """
    Contacts the DB to fetch the info.
    Returns a pd.DataFrame with the response. 
    """
    async with db_pool.acquire(timeout=180) as connection:
        response = []
        try: 
            query = f"""SELECT * FROM {DB_SCHEMA}.query_patients({create_prepstmt_variables(14)});"""
            LOG.debug(f"QUERY to fetch hits: {query}")
            statement = await connection.prepare(query)
            db_response = await statement.fetch(*query_parameters)         

            for record in list(db_response):
                response.append(dict(record))

        except Exception as e:
                raise BeaconServerError(f'Query individuals DB error: {e}') 

        if response:
            # Converting the response to a DataFrame 
            response_df = pd.DataFrame(response)
            # Making sure we don't have NaN values
            response_df = response_df.where(response_df.notnull(), None)

            return True, response_df
        else:
            LOG.debug(f"No response for this query on the {endpoint} endpoint.")
            return False, []


def request2queryparameters(raw_request):
    """
    Reorganize the request to match the query_patients() SQL function input.
    """

    ## We create a list of the parameters that the SQL function needs
    correct_parameters =  [
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
    "individualId",  # _individual_stable_id text
    "filters"]  # _filters text
    
    int_params = ['start', 'end', 'endMax', 'endMin', 'startMax', 'startMin']

    ## Iterate correct_parameters to create the query_parameters list from the raw_request 
    ## in the required order and with the right types
    query_parameters = []

    for param in correct_parameters:
        query_param = raw_request.get(param)
        if query_param:  # control if the user has used the parameter
            if param in int_params:
                query_parameters.append(int(query_param))
            else:
                query_parameters.append(str(query_param))
        else:
            if param in int_params:
                query_parameters.append(None)
            else:
                query_parameters.append("null")

    # At this point we have a list with the needed parameters called query_parameters, the only thing 
    # laking is to update the datasetsIds (it can be "null" or what the user specified)
    LOG.debug(f"Raw param: {dict(raw_request)}")
    LOG.debug(f"Raw param types: {[type(x) for x in dict(raw_request)]}")
    LOG.debug(f"Correct param: {correct_parameters}")
    LOG.debug(f"Query param: {query_parameters}")
    LOG.debug(f"Query param types: {[type(x) for x in query_parameters]}")

    return query_parameters


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def get_individuals_rest(db_pool, request):
    """
    Main function of the endpoint. 
    """

    # 1. REQUEST PROCESSING
    
    # Get the raw request
    raw_request = dict(request.rel_url.query)

    # Add individualId parameter if used
    if dict(request.match_info):
        individual_id = request.match_info['target_id_req']
        raw_request.update({"individualId": individual_id})

    # Prepare pagination
    skip = raw_request.get("skip", 0)
    limit = raw_request.get("limit", 10)
    raw_request.update({"skip": skip, "limit": limit})

    # Parse the request to prepare it to be used in the SQL function
    query_parameters = request2queryparameters(raw_request)

    # Also check request to see if there is any alternativeSchema
    alternative_schemas_req = raw_request.get("individualSchemas")
    alternative_schemas = alternative_schemas_req.split(",") if alternative_schemas_req else []

    # 2. GET VALID/ACCESSIBLE DATASETS

    # We want to get a list of the datasets available in the database separated in three lists
    # depending on the access level (we check all of them if the user hasn't specified anything, if some
    # there were given, those are the only ones that are checked)
    request_datasets = query_parameters[-3]
    public_datasets, registered_datasets, controlled_datasets = await fetch_datasets_access(db_pool, request_datasets)

    ##### TEST CODE TO USE WHEN AAI is integrated
    # access_type, accessible_datasets = access_resolution(request, request['token'], request.host, public_datasets,
    #                                                      registered_datasets, controlled_datasets)
    # LOG.info(f"The user has this types of access: {access_type}")
    # query_parameters[-3] = ",".join([str(id) for id in accessible_datasets])
    ##### END TEST

    # NOTE that right now we will just focus on the PUBLIC ones to ease the process, so we get all their 
    # ids and add them to the SQL query parameters
    query_parameters[-3] = ",".join([str(id) for id in public_datasets])  # e.g. '1,2,3'

    LOG.info(f"Query FINAL param: {query_parameters}")

    # 3. RETRIEVE DATA FROM THE DB (use SQL function)

    LOG.info('Connecting to the DB to make the query.')
    exists, response_df = await get_result(db_pool, query_parameters)
    LOG.info('Query done.')
    
    # 4. CREATE INDIVIDUALS OBJECT
    LOG.info('Shaping the DB response.')
    if exists:
        results = create_individuals_object(response_df, alternative_schemas)
    else:
        results = response_df
    LOG.info('Arrangement done.')

    # 5. CREATE FINAL RESPONSE
    LOG.info('Creating the final response.')
    final_response = create_final_response(raw_request, results)
    LOG.info('Done.')
    return final_response