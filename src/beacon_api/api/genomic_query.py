"""
Genomic SNP and REGION endpoint.

This endpoint is specific for querying a specific subset of variant or all variants that appear in a certain region, hence the 
parameters accepted by the request differ from the ones in the basic query endpoint.

.. note:: See ``schemas/genomic_region.json`` for checking the parameters accepted in the region endpoint.
.. note:: See ``schemas/genomic_snp.json`` for checking the parameters accepted in the snp endpoint.
"""

import ast
import logging

from .exceptions import BeaconBadRequest, BeaconServerError, BeaconForbidden, BeaconUnauthorised
from .. import __apiVersion__, __id__
from ..conf.config import DB_SCHEMA

from ..utils.polyvalent_functions import create_prepstmt_variables, filter_exists, datasetHandover
from ..utils.polyvalent_functions import prepare_filter_parameter, parse_filters_request
from ..utils.polyvalent_functions import fetch_datasets_access, access_resolution

from ..utils.polyvalent_functions import filter_response, snp_resultsHandover, fetch_variantAnnotations
from .access_levels import ACCESS_LEVELS_DICT
from ..utils.translate2accesslevels import region2access, snp2access
from ..utils.models import variant_object, variantAnnotation_object

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
                        WHERE id={dict(record).get("dataset_id")};
                        """
            statement = await connection.prepare(query)
            extra_record = await statement.fetchrow()
        except Exception as e:
            raise BeaconServerError(f'Query metadata (stableID) DB error: {e}') 

    response = dict(record)

    for dispensable in ["id", "variant_id", "variant_composite_id", "chromosome", "reference", "alternate", "start", "end", "variant_type"]:
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
                        "matchingSampleCount": 0 }
    response["datasetHandover"] = datasetHandover(dataset_name)
    return response



# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN QUERY TO THE DATABASE
# ----------------------------------------------------------------------------------------------------------------------

async def fetch_resulting_datasets(db_pool, query_parameters, misses=False, accessible_missing=None):
    """
    Contact the DB to fetch the information about the datasets. 

    :misses: set to True for retrieving data about datasets without the queried variant
    :accessible_missing: list of accessible datasets without the variant.

    Returns list of datasets dictionaries. 
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
                processed = transform_misses(record) if misses else record
                datasets.append(processed)
            return datasets
        except Exception as e:
                raise BeaconServerError(f'Query resulting datasets DB error: {e}') 
    


async def get_datasets(db_pool, query_parameters, include_dataset, processed_request):
    """
    Find datasets based on query parameters.
    """
    all_datasets = []
    dataset_ids = query_parameters[-2]

    # Fetch the records of all the hit datasets
    all_datasets = await fetch_resulting_datasets(db_pool, query_parameters)

    # Then parse the records to be able to separate them by variants, note that we add the hit records already transformed to form the datasetAlleleResponses
    variants_dict = {}
    for record in all_datasets:
        variant_identifier = record.get("variant_composite_id")
        # If the DB doens't have a unique variant identifier, we construct one
        # important_parameters = map(str, [record.get("chromosome"), record.get("variant_id"), record.get("reference"), record.get("alternate"), record.get("start"), record.get("end"), record.get("variant_type")])
        # variant_identifier = "|".join(important_parameters)

        if variant_identifier not in variants_dict.keys():
            variants_dict[variant_identifier] = {}
            variants_dict[variant_identifier]["variantDetails"] = {
                "variantId": record.get("variant_id"),
                "referenceName":  record.get("chromosome"),
                "referenceBases": record.get("reference"),
                "alternateBases": record.get("alternate"),
                "variantType": record.get("variant_type"),
                "start": record.get("start"), 
                "end": record.get("end")
            }
            variants_dict[variant_identifier]["datasetAlleleResponses"] = []
            variants_dict[variant_identifier]["datasetAlleleResponses"].append(await transform_record(db_pool, record))
        else:
            variants_dict[variant_identifier]["datasetAlleleResponses"].append(await transform_record(db_pool, record))

    # If  the includeDatasets option is ALL or MISS we have to "create" the miss datasets (which will be tranformed also) and join them to the datasetAlleleResponses
    if include_dataset in ['ALL', 'MISS']:
        for variant in variants_dict:
            list_hits = [record["internalId"] for record in variants_dict[variant]["datasetAlleleResponses"]]
            list_all = list(map(int, dataset_ids.split(",")))
            accessible_missing = [int(x) for x in list_all if x not in list_hits]
            miss_datasets = await fetch_resulting_datasets(db_pool, query_parameters, misses=True, accessible_missing=accessible_missing)
            variants_dict[variant]["datasetAlleleResponses"] += miss_datasets

    # Finally, we iterate the variants_dict to create the response
    response = []
    for variant in variants_dict:
        rsID, cellBase_dict, dbSNP_dict = await fetch_variantAnnotations(variants_dict[variant]["variantDetails"])
        if rsID: variants_dict[variant]["variantDetails"]["variantId"] = rsID
        datasetAlleleResponses = filter_exists(include_dataset, variants_dict[variant]["datasetAlleleResponses"])
        final_variantsFound_element = {
            "variant": variant_object(processed_request, variants_dict[variant]["variantDetails"]),
            # "variantDetails": variants_dict[variant]["variantDetails"],
            "datasetAlleleResponses": datasetAlleleResponses,
            "variantAnnotations": variantAnnotation_object(processed_request, cellBase_dict, dbSNP_dict, {}),
            "variantHandover": snp_resultsHandover(rsID) if rsID else '',
            "info": {}
        }

        response.append(final_variantsFound_element)

    return response
    

# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def genomic_request_handler(db_pool, processed_request, request):
    """
    Construct the Query response. 

    Process and prepare the parameters, fetch dataset access information, execute
    main queries and prepare the response object. 
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

    ##### TEST CODE TO USE WHEN AAI is integrated
    # access_type, accessible_datasets = access_resolution(request, request['token'], request.host, public_datasets,
    #                                                      registered_datasets, controlled_datasets)
    # LOG.info(f"The user has this types of acces: {access_type}")
    # query_parameters[-2] = ",".join([str(id) for id in accessible_datasets])
    ##### END TEST

    # NOTE that rigth now we will just focus on the PUBLIC ones to easen the process, so we get all their 
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

    variantsFound = await get_datasets(db_pool, query_parameters, include_dataset, processed_request)

    LOG.info('Query done.')

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
                    "value": { 'beaconId': __id__,
                        'apiVersion': __apiVersion__,
                        'exists': any([dataset['exists'] for variant in variantsFound for dataset in variant["datasetAlleleResponses"]]),
                        'request': { "meta": { "request": {
                                                            "Variant": ["beacon-variant-v0.1"]  + variant,
                                                            "VariantAnnotation": ["beacon-variant-annotation-v1.0"] + variantAnnotation,
                                                            "VariantMetadata": ["beacon-variant-metadata-v1.0"] + variantMetadata
                                                        },
                                                "apiVersion": __apiVersion__,
                                            },
                                    "query": query
                                    },
                        'variantsFound': variantsFound,
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
    # NOTE we hardcode accessible_datasets and user_levels it because authentication is not implemented yet
    accessible_datasets = public_datasets
    user_levels = ["PUBLIC"]

    url_endpoint = str(request.rel_url)
    if url_endpoint.startswith('/genomic_region'):
        beacon_response = {"beaconGenomicRegionRequest": beacon_response}  # Make sure the key matches the name in the access levels dict
        filtered_response = filter_response(beacon_response, ACCESS_LEVELS_DICT, accessible_datasets, user_levels, region2access)
    else:
        beacon_response = {"beaconGenomicSnpRequest": beacon_response}  # Make sure the key matches the name in the access levels dict
        filtered_response = filter_response(beacon_response, ACCESS_LEVELS_DICT, accessible_datasets, user_levels, snp2access)

    return filtered_response["beaconGenomicRegionRequest"]