"""
Genomic SNP endpoint

This endpoint is specific for querying SNPs, hence the parameters accepted by the request 
differ from the ones in the basic query endpoint.
"""

import ast
import logging

from .exceptions import BeaconBadRequest, BeaconServerError, BeaconForbidden, BeaconUnauthorised
from .. import __apiVersion__
from ..conf.config import DB_SCHEMA

from ..utils.polyvalent_functions import create_prepstmt_variables, filter_exists, datasetHandover
from ..utils.polyvalent_functions import prepare_filter_parameter, parse_filters_request
from ..utils.polyvalent_functions import fetch_datasets_access, access_resolution

from ..utils.polyvalent_functions import filter_response, snp_resultsHandover, fetch_variantAnnotations
from .access_levels import ACCESS_LEVELS_DICT
from ..utils.translate2accesslevels import snp2access
from ..utils.models import variant_object, variantAnnotation_object


LOG = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
#                                         FORMATTING
# ----------------------------------------------------------------------------------------------------------------------

def create_variantsFound(processed_request, datasets, variant_id, variant_annotations):
    """
    Format the response inside a variantsFound object that will be a list containing ONLY one item (similar to genomic_region's same named function)
    """
    variantsFound = [ 
                        {
                        "variant": variant_object(processed_request, processed_request, variantId = variant_id),  # we repeat processed_request beacause in the SNP case, in the second parameter it represents the variant_details
                        "variantAnnotations": variant_annotations,
                        "variantHandover": snp_resultsHandover(variant_id) if variant_id else '',
                        "datasetAlleleResponses": datasets
                        }
                        ]

    return variantsFound



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

    for dispensable in ["id", "variant_composite_id", "chromosome", "reference", "alternate", "start", "end", "variant_type"]:
        response.pop(dispensable)

    dataset_name = dict(extra_record).pop("stable_id")   
    response["datasetId"] = dataset_name
    response["internalId"] = response.pop("dataset_id")
    response["exists"] = True
    response["variantCount"] = response.pop("variant_cnt")  
    response["callCount"] = response.pop("call_cnt") 
    response["sampleCount"] = response.pop("sample_cnt") 
    response["frequency"] = 0 if response.get("frequency") is None else float(response.pop("frequency"))
    response["numVariants"] = 0 if response.get("num_variants") is None else response.pop("num_variants")
    response["info"] = {"accessType": dict(extra_record).pop("access_type"),
                        "matchingSampleCount": 0 if response.get("matching_sample_cnt") is None else response.pop("matching_sample_cnt")}
    response["datasetHandover"] = datasetHandover(dataset_name)
    response["variantId"] = None if response.get("variant_id") == "." else response.pop("variant_id")
    
    return response


def transform_misses(record):
    """Format the missed datasets record we got from the database to adhere to the response schema."""
    response = {}

    dataset_name = dict(record).get("stableId") 

    response["datasetId"] = dataset_name 
    response["internalId"] = dict(record).get("datasetId")
    response["exists"] = False
    # response["datasetId"] = ''  
    response["variantCount"] = 0
    response["callCount"] = 0
    response["sampleCount"] = 0
    response["frequency"] = 0 
    response["numVariants"] = 0 
    response["info"] = {"accessType": dict(record).get("accessType"),
                        "matchingSampleCount": 0 if record.get("matching_sample_cnt") is None else record.get("matching_sample_cnt")}
    response["datasetHandover"] = datasetHandover(dataset_name)
    response["variantId"] = None if record.get("variant_id") == "." else record.get("variant_id")

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
                query = f"""SELECT * FROM {DB_SCHEMA}.query_data_response({create_prepstmt_variables(13)});"""
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

async def snp_request_handler(db_pool, processed_request, request):
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
        filters_request_list = ast.literal_eval(query_parameters[-1])
        processed_filters_param, _ = await prepare_filter_parameter(db_pool, filters_request_list)
        query_parameters[-1] = 'null' if not processed_filters_param else processed_filters_param

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

    # Get the varianstAnnotations handovers and create the object
    rsID, cellBase_dict, dbSNP_dict = await fetch_variantAnnotations(processed_request)
    variant_annotations = variantAnnotation_object(processed_request, cellBase_dict, dbSNP_dict, {})

    # Get the variantId to show it in the resultsHanover section
    variantId = list(set([dataset.get("variantId") for dataset in datasets if dataset.get("variantId") != None]))
    if len(variantId) > 1:
        LOG.debug(f"More than one variantId found: {variantId}. Using just the first one.")

    variantId = rsID if not variantId else str(variantId[0])
    LOG.debug(f"VariantId: {variantId}")
   
    # Create the query object to show it in the response
    query = processed_request.copy()
    if query.get("variant"):
        query.pop("variant")
    
    # Make lists of the models requests to show it in the response
    variant = processed_request.get("variant").split(",") if processed_request.get("variant") else []
    variantAnnotation = processed_request.get("variantAnnotation").split(",") if processed_request.get("variantAnnotation") else [] 
    variantMetadata = processed_request.get("variantMetadata").split(",") if processed_request.get("variantMetadata") else [] 

    # We create the final dictionary with all the info we want to return
    beacon_response = {
                    "meta": {
                        "Variant": ["beacon-variant-v0.1", "ga4gh-variant-representation-v0.1"],
  	                    "VariantAnnotation": ["beacon-variant-annotation-v1.0"],
                        "VariantMetadata": ["beacon-variant-metadata-v1.0"]
                    },
                    "value":   { 'beaconId': '.'.join(reversed(request.host.split('.'))),
                        'apiVersion': __apiVersion__,
                        'exists': any([x['exists'] for x in datasets]),
                        # Error is not required and should not be shown unless exists is null
                        # If error key is set to null it will still not validate as it has a required key errorCode
                        # Setting this will make schema validation fail
                        # "error": None,
                        'request': { "meta": { "request": {
                                                            "Variant": ["beacon-variant-v0.1"]  + variant,
                                                            "VariantAnnotation": ["beacon-variant-annotation-v1.0"] + variantAnnotation,
                                                            "VariantMetadata": ["beacon-variant-metadata-v1.0"] + variantMetadata
                                                        },
                                                "apiVersion": __apiVersion__,
                                            },
                                    "query": query
                                    },
                        'variantsFound': create_variantsFound(processed_request, filter_exists(processed_request.get("includeDatasetResponses", "NONE"), datasets), variantId, variant_annotations),
                        'info': None,
                        'resultsHandover': None,
                        'beaconHandover': [ { "handoverType" : {
                                                "id" : "CUSTOM",
                                                "label" : "Organization contact"
                                                },
                                                "note" : "Organization contact details maintaining this Beacon",
                                                "url" : "mailto:beacon.ega@crg.eu"
                                            } ]
                        
                        }
                    }

    # Before returning the response we need to filter it depending on the access levels
    beacon_response = {"beconGenomicSnpRequest": beacon_response}  # Make sure the key matches the name in the access levels dict
    
    # NOTE we hardcode accessible_datasets and user_levels it because authentication is not implemented yet
    accessible_datasets = public_datasets
    user_levels = ["PUBLIC"]  
    filtered_response = filter_response(beacon_response, ACCESS_LEVELS_DICT, accessible_datasets, user_levels, snp2access)
    
    return filtered_response["beconGenomicSnpRequest"]
