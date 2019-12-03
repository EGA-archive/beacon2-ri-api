"""
Query endpoint

Basic query endpoint in the beacon.
"""


import ast
import logging

from .exceptions import BeaconBadRequest, BeaconServerError, BeaconForbidden, BeaconUnauthorised
from .. import __apiVersion__
from ..conf.config import DB_SCHEMA

from ..utils.polyvalent_functions import create_prepstmt_variables, filter_exists
from ..utils.polyvalent_functions import prepare_filter_parameter, parse_filters_request
from ..utils.polyvalent_functions import fetch_datasets_access, access_resolution

from ..utils.polyvalent_functions import filter_response
from .access_levels import ACCESS_LEVELS_DICT
from ..utils.translate2accesslevels import query2access

LOG = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
#                                         FORMATTING
# ----------------------------------------------------------------------------------------------------------------------

async def transform_record(db_pool, record):
    """Format the record we got from the database to adhere to the response schema."""

    # Before creating the dict, we want to get the stable_id frm the DB
    async with db_pool.acquire(timeout=180) as connection:
        try: 
            query = f"""SELECT stable_id, access_type
                        FROM beacon_dataset
                        WHERE id={dict(record).pop("dataset_id")};
                        """
            statement = await connection.prepare(query)
            extra_record = await statement.fetchrow()
        except Exception as e:
            raise BeaconServerError(f'Query metadata (stableID) DB error: {e}') 

    response = dict(record)

    response.pop("id")
    response["datasetId"] = dict(extra_record).pop("stable_id")  
    response["internalId"] = response.pop("dataset_id")
    response["exists"] = True
    response["variantCount"] = response.pop("variant_cnt")  
    response["callCount"] = response.pop("call_cnt") 
    response["sampleCount"] = response.pop("sample_cnt") 
    response["frequency"] = 0 if response.get("frequency") is None else float(response.pop("frequency"))
    response["numVariants"] = 0 if response.get("num_variants") is None else response.pop("num_variants")
    response["info"] = {"access_type": dict(extra_record).pop("access_type")}   
    
    return response


def transform_misses(record):
    """Format the missed datasets record we got from the database to adhere to the response schema."""
    response = {}
    response["datasetId"] = dict(record).get("stableId")  
    response["internalId"] = dict(record).get("datasetId")
    response["exists"] = False
    # response["datasetId"] = ''  
    response["variantCount"] = 0
    response["callCount"] = 0
    response["sampleCount"] = 0
    response["frequency"] = 0 
    response["numVariants"] = 0 
    response["info"] = {"access_type": dict(record).get("accessType")}

    return response



# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN QUERY TO THE DATABASE
# ----------------------------------------------------------------------------------------------------------------------

async def fetch_resulting_datasets(db_pool, query_parameters, misses=False, accessible_missing=None):
    """Find datasets based on filter parameters.
    """
    async with db_pool.acquire(timeout=180) as connection:
        datasets = []
        try: 
            if misses:
                if accessible_missing:
                    query = f"""SELECT id as "datasetId", access_type as "accessType", stable_id as "stableId"
                                FROM beacon_dataset
                                WHERE id IN ({create_prepstmt_variables(len(accessible_missing))});
                                """
                    # LOG.debug(f"QUERY to fetch accessible missing info: {query}")
                    statement = await connection.prepare(query)
                    db_response =  await statement.fetch(*accessible_missing)
                else:
                    return []
            else:
                query = f"""SELECT * FROM {DB_SCHEMA}.query_data_summary_response({create_prepstmt_variables(13)});"""
                LOG.debug(f"QUERY to fetch hits: {query}")
                statement = await connection.prepare(query)
                db_response = await statement.fetch(*query_parameters)         

            for record in list(db_response):
                processed = transform_misses(record) if misses else await transform_record(db_pool, record)
                datasets.append(processed)
            return datasets
        except Exception as e:
                raise BeaconServerError(f'Query resulting datasets DB error: {e}') 

    

async def get_datasets(db_pool, query_parameters, include_dataset):
    """Find datasets based on filter parameters.
    """
    hit_datasets = []
    miss_datasets = []
    response = []
    dataset_ids = query_parameters[-2]

    hit_datasets = await fetch_resulting_datasets(db_pool, query_parameters)
    LOG.debug(f"hit_datasets: {hit_datasets}")

    if include_dataset in ['ALL', 'MISS']:
        list_all = list(map(int, dataset_ids.split(",")))
        LOG.debug(f"list_all: {list_all}")
        list_hits  =  [dict["internalId"] for dict in hit_datasets]
        LOG.debug(f"list_hits: {list_hits}")
        accessible_missing = [int(x) for x in list_all if x not in list_hits]
        LOG.debug(f"accessible_missing: {accessible_missing}")
        miss_datasets = await fetch_resulting_datasets(db_pool, query_parameters, misses=True, accessible_missing=accessible_missing)
    response = hit_datasets + miss_datasets
    return response


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def query_request_handler(db_pool, processed_request, request):
    """
    Execute query with SQL funciton.
    """
    # First we parse the query to prepare it to be used in the SQL function
    # We create a list of the parameters that the SQL function needs
    correct_parameters =  [
	"variantType",
	"start",
	"startMin",
	"startMax",
	"end",
	"endMin",
	"endMax",
	"referenceName",
	"referenceBases",
	"alternateBases",
	"assemblyId",
	"datasetIds",
    "filters"]
    
    int_params = ['start', 'end', 'endMax', 'endMin', 'startMax', 'startMin']

    query_parameters = []

    # Iterate correct_parameters to create the query_parameters list from the processed_request 
    # in the requiered order and with the right types
    for param in correct_parameters:
        query_param = processed_request.get(param)
        if query_param:
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
    # laking is to update the datasetsIds (it can be "null" or processed_request.get("datasetIds"))

    LOG.debug(f"Correct param: {correct_parameters}")
    LOG.debug(f"Query param: {query_parameters}")
    LOG.debug(f"Query param types: {[type(x) for x in query_parameters]}")

    # We want to get a list of the datasets available in the database separated in three lists
    # depending on the access level (we check all of them if the user hasn't specified anything, if some
    # there were given, those are the only ones that are checked)
    public_datasets, registered_datasets, controlled_datasets = await fetch_datasets_access(db_pool, query_parameters[-2])

    ##### TEST
    # access_type, accessible_datasets = access_resolution(request, request['token'], request.host, public_datasets,
    #                                                      registered_datasets, controlled_datasets)
    # LOG.info(f"The user has this types of acces: {access_type}")
    # query_parameters[-2] = ",".join([str(id) for id in accessible_datasets])
    ##### END TEST

    # NOTICE that rigth now we will just focus on the PUBLIC ones to easen the process, so we get all their 
    # ids and add them to the query
    query_parameters[-2] = ",".join([str(id) for id in public_datasets])

    # We adapt the filters parameter to be able to use it in the SQL function (e.g. '(technology)::jsonb ?& array[''Illumina Genome Analyzer II'', ''Illumina HiSeq 2000'']')
    if query_parameters[-1] != "null":
        processed_filters_param, _ = await prepare_filter_parameter(db_pool, query_parameters[-1])
        query_parameters[-1]  = processed_filters_param

    # We will output the datasets depending on the includeDatasetResponses parameter
    include_dataset = ""
    if processed_request.get("includeDatasetResponses"):
        include_dataset  = processed_request.get("includeDatasetResponses")
    else:
        include_dataset  = "ALL"

    LOG.info(f"Query FINAL param: {query_parameters}")
    LOG.info('Connecting to the DB to make the query.')
    datasets = await get_datasets(db_pool, query_parameters, include_dataset)
    LOG.info('Query done.')

    # We create the final dictionary with all the info we want to return
    beacon_response = { 'beaconId': '.'.join(reversed(request.host.split('.'))),
                        'apiVersion': __apiVersion__,
                        'exists': any([x['exists'] for x in datasets]),
                        # Error is not required and should not be shown unless exists is null
                        # If error key is set to null it will still not validate as it has a required key errorCode
                        # Setting this will make schema validation fail
                        # "error": None,
                        'info': None,
                        'alleleRequest': processed_request,
                        'datasetAlleleResponses': filter_exists(include_dataset, datasets)}
    
    # Before returning the response we need to filter it depending on the access levels
    beacon_response = {"beaconAlleleResponse": beacon_response}

    # NOTE we hardcode accessible_datasets and user_levels it because authentication is not implemented yet
    accessible_datasets = public_datasets
    user_levels = ["PUBLIC"]  
    filtered_response = filter_response(beacon_response, ACCESS_LEVELS_DICT, accessible_datasets, user_levels, query2access)

    return filtered_response["beaconAlleleResponse"]
