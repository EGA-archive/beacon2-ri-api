import ast
import logging
import requests

from .exceptions import BeaconBadRequest, BeaconServerError, BeaconForbidden, BeaconUnauthorised
from .. import __apiVersion__
from ..conf.config import DB_SCHEMA

from ..utils.polyvalent_functions import create_prepstmt_variables, filter_exists, datasetHandover
from ..utils.polyvalent_functions import prepare_filter_parameter, parse_filters_request
from ..utils.polyvalent_functions import fetch_datasets_access, access_resolution
from ..utils.models import variant_object, variantAnnotation_object

from .genomic_region import fetch_resulting_datasets, fetch_variantAnnotations, snp_resultsHandover


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

    for dispensable in ["id", "variant_id", "chromosome", "reference", "alternate", "start", "end"]:
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

def create_query(processed_request):
    """
    Restructure the request to build the query object
    """
    query = {
        "variant": {
            "referenceBases": "" if not processed_request.get("referenceBases") else processed_request.get("referenceBases"),
            "alternateBases": "" if not processed_request.get("alternateBases") else processed_request.get("alternateBases"),
            "referenceName": "" if not processed_request.get("referenceName") else processed_request.get("referenceName"),
            "start": None if not processed_request.get("start") else processed_request.get("start"),
            "end": None if not processed_request.get("end") else processed_request.get("end"),
            "assemblyId": "" if not processed_request.get("assemblyId") else processed_request.get("assemblyId")
            },
        "datasets": {
            "datasetIds": None if not processed_request.get("datasetIds") else processed_request.get("datasetIds"),
            "includeDatasetResponses": "ALL" if not processed_request.get("includeDatasetResponses") else processed_request.get("includeDatasetResponses")
             },
    "filters": None if not processed_request.get("filters") else processed_request.get("filters"),
    "customFilters": None
    }

    return query

# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

async def create_variantsFound(db_pool, processed_request, records_list, valid_datasets, include_dataset):
    """
    Function based on the variantsFound creation done in the genomicRegion endpoint.
    Takes a list of records and returns them structured as the variantsFoun object.

    Notice in this case we will still have to filter out by variant later on (if that's the case).
    """
    all_datasets = []
    dataset_ids = valid_datasets

    # Fetch the records 
    all_datasets = records_list

    # Then parse the records to be able to separate them by variants, note that we add the hit records already transformed to form the datasetAlleleResponses
    variants_dict = {}
    for record in all_datasets:
        important_parameters = map(str, [record.get("chromosome"), record.get("variant_id"), record.get("reference"), record.get("alternate"), record.get("start"), record.get("end"), record.get("variant_type")])
        variant_identifier = "|".join(important_parameters)
        # variant_identifier = record.get("variant_composite_id")

        if variant_identifier not in variants_dict.keys():
            variants_dict[variant_identifier] = {}
            variants_dict[variant_identifier]["variantDetails"] = {
                "variantId": record.get("variant_id"),
                "chromosome":  record.get("chromosome"),
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
            list_all = dataset_ids
            accessible_missing = [int(x) for x in list_all if x not in list_hits]
            miss_datasets = await fetch_resulting_datasets(db_pool, "", misses=True, accessible_missing=accessible_missing)
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





async def get_valid_datasets(db_pool, dataset_filters):
    """
    Returns a list of the dataset ids that pass the filters
    """
    async with db_pool.acquire(timeout=180) as connection:
        id_list = []
        try: 
            if dataset_filters:
                query  = f"""SELECT id
                            FROM beacon_dataset_table
                            WHERE {dataset_filters};"""
            else:
                query  = f"""SELECT id
                            FROM beacon_dataset_table;"""


            LOG.debug(f"QUERY samples filtered: {query}")
            statement = await connection.prepare(query)
            db_response = await statement.fetch()

            for record in list(db_response):
                id_list.append(dict(record).get("id"))

        except Exception as e:
            raise BeaconServerError(f'Query filtered datasets DB error: {e}')

    return id_list
       


async def join_data2sample(db_pool, samples_dict, valid_datasets, processed_request):
    """
    Iterates through the samples dict and connects to the DB to
    gather the info of the variants associated and join it to the dict
    """
    # Gathering the variant related parameters passed in the request
    chromosome = '' if not processed_request.get("referenceName") else processed_request.get("referenceName") 
    reference = '' if not processed_request.get("referenceBases") else processed_request.get("referenceBases") 
    alternate = '' if not processed_request.get("alternateBases") else processed_request.get("alternateBases")
    start = 'null' if not processed_request.get("start") else processed_request.get("start")
    end = 'null' if not processed_request.get("end") else processed_request.get("end")

    valid_datasets = ",".join([str(i) for i in valid_datasets])
    for key, value in samples_dict.items():

        samples_dict[key]["variants"] = []
        async with db_pool.acquire(timeout=180) as connection:
            try:
                if start != 'null': 
                    query = f"""SELECT * FROM v20.beacon_data_table d 
                                JOIN v20.beacon_dataset_sample_table c 
                                ON d.dataset_id = c.dataset_id 
                                WHERE d.dataset_id IN ({valid_datasets}) 
                                AND sample_id = {key}
                                AND (CASE
                                    WHEN nullif('{chromosome}', '') IS NOT NULL THEN chromosome = '{chromosome}' ELSE true
                                    END)
                                AND (CASE
                                    WHEN nullif('{reference}', '') IS NOT NULL THEN reference = '{reference}' ELSE true
                                    END)
                                AND (CASE
                                    WHEN nullif('{alternate}', '') IS NOT NULL THEN alternate = '{alternate}' ELSE true
                                    END)
                                AND (CASE
                                    WHEN {start} IS NOT NULL THEN start = {start} ELSE true
                                    END)
                                AND (CASE
                                    WHEN {end} IS NOT NULL THEN 'end' = {end} ELSE true
                                    END);
                                """
                else:
                    # query  = f"""SELECT * FROM 
                    #             (SELECT * FROM beacon_data_table d 
                    #             JOIN beacon_dataset_sample_table c 
                    #             ON d.dataset_id = c.dataset_id WHERE d.dataset_id IN ({valid_datasets})) 
                    #             AS joined_datasample WHERE sample_id = {key};"""
                    query  = f"""SELECT * FROM beacon_data_table d 
                                JOIN beacon_dataset_sample_table c 
                                ON d.dataset_id = c.dataset_id WHERE d.dataset_id IN ({valid_datasets}) 
                                AND sample_id = {key} LIMIT 5;"""

                LOG.debug(f"QUERY variants per sample: {query}")
                statement = await connection.prepare(query)
                db_response = await statement.fetch()

                for record in list(db_response):
                    samples_dict[key]["variants"].append(record)

            except Exception as e:
                raise BeaconServerError(f'Query filtered samples DB error: {e}')
    return samples_dict



async def get_samples(db_pool, filters_dict):
    """
    Function that creates a dict of the samples and their info while filtering
    out by the filters given in the request (related to sample and to patient).
    """
    # Preparing the SQL query with the clauses based on the requests
    sentence = []
    target_table_sample = f"{DB_SCHEMA}.beacon_sample_table"
    target_table_patient = f"{DB_SCHEMA}.patient_table"
    samples_filter_dict = None if not filters_dict.get(target_table_sample) else filters_dict.get(target_table_sample)
    patients_filter_dict = None if not filters_dict.get(target_table_patient) else filters_dict.get(target_table_patient)

    if samples_filter_dict:
        for column, list_values in samples_filter_dict.items():
            sentence_part = f""" s.{column} IN ('{"','".join(list_values)}')"""
            sentence.append(sentence_part)
    if patients_filter_dict:
        for column, list_values in patients_filter_dict.items():
            sentence_part = f""" p.{column} IN ('{"','".join(list_values)}')"""
            sentence.append(sentence_part)
    
    sentence = " AND ".join(sentence)
    sentence_exists = False if not sentence else True

    # Fetching the samples and its patient info
    async with db_pool.acquire(timeout=180) as connection:
        response = []
        try:
            query  = f"""SELECT s.id as sample_id, s.stable_id as sample_stable_id, s.sex, s.tissue, s.description, 
                        p.id as patient_id, p.stable_id as patient_stable_id, p.age_of_onset, p.disease 
                        FROM beacon_sample_table s 
                        JOIN patient_table p ON s.patient_id = p.id 
                        WHERE (CASE WHEN {sentence_exists} THEN {sentence} ELSE true END) AND s.sex IS NOT NULL;"""

            LOG.debug(f"QUERY samples: {query}")
            statement = await connection.prepare(query)
            db_response = await statement.fetch()

            response = []
            for record in list(db_response):
                response.append(dict(record))
        except Exception as e:
            raise BeaconServerError(f'Query filtered samples DB error: {e}')

    # Creating a samples dict with sample and patient as keys and their info as values
    samples_dict = {}
    for record in response:
        samples_dict[record["sample_id"]] = {}
        one_sample_dict = {
            "sample": {
                "id": record.get("sample_id"),
                "stableId": record.get("sample_stable_id"),
                "sex": record.get("sex"),
                "tissue": record.get("tissue"),
                "description": record.get("description"),
            },
            "patient": {
                "id": record.get("patient_id"),
                "stableId": record.get("patient_stable_id"),
                "ageOfOnset": record.get("age_of_onset"),
                "disease": record.get("disease"),
            }
        }
        samples_dict[record["sample_id"]] = one_sample_dict

    return samples_dict



# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def sample_request_handler(db_pool, processed_request, request):
    """
    Execute query with SQL funciton.
    """

    # First we are going to get the lists of the available datasets
    public_datasets, registered_datasets, controlled_datasets = await fetch_datasets_access(db_pool, processed_request.get("datasetIds"))

        ##### TEST
        # access_type, accessible_datasets = access_resolution(request, request['token'], request.host, public_datasets, registered_datasets, controlled_datasets)
        # LOG.info(f"The user has this types of acces: {access_type}")
        # query_parameters[-2] = ",".join([str(id) for id in accessible_datasets])
        ##### END TEST

    # NOTICE that rigth now we will just focus on the PUBLIC ones to easen the process, so we get all their ids and add them to the query
    available_datasets = public_datasets

    # We will output the datasets depending on the includeDatasetResponses parameter
    include_dataset = ""
    if processed_request.get("includeDatasetResponses"):
        include_dataset  = processed_request.get("includeDatasetResponses")
    else:
        include_dataset  = "ALL"

    # Then we are going to parse the filters to separate them depending on their target table
    if processed_request.get("filters"):
        dataset_filters, filters_dict = await prepare_filter_parameter(db_pool, processed_request.get("filters"))
    else:
        dataset_filters = ""
        filters_dict = {}
        

    # Now we want to filter the sample table and get a dict with the samples that passed the filters and their info
    samples_dict = await get_samples(db_pool, filters_dict)

    # we'll need to apply the dataset related filters (if there is any) so we are going to generate a list
    # with the ones that pass the filters
    valid_datasets = await get_valid_datasets(db_pool, dataset_filters)

    # The intersection between the datasets that are available by access and the datasets that have passed the filters
    # is the final list of valid_datasets
    valid_datasets = [dataset for dataset in valid_datasets if dataset in available_datasets]

    # We want to join the sample information with its data (variants) using the dataset it comes from
    # The result will be the dict with sample_id as key and the value is another dict with two keys "sample"
    # with the sample info and "variants" that is a list of the records of each variant from beacon_data_table
    # Notice we get only the datasets that have passed the filters
 
    samples_dict = await join_data2sample(db_pool, samples_dict, valid_datasets, processed_request)

    # Finally, we want to build the results list, which is a list of dicts, each dict representing a sample
    # with the sample object, the variantsFound object and the patients object
    results = []
    for sample in samples_dict.keys():
        sample_object = {"version": "beacon-sample-v1.0",
                        "value": {
                            "id": samples_dict[sample]["sample"].get("id"),
                            "sex": samples_dict[sample]["sample"].get("sex"),
                            "tissue": samples_dict[sample]["sample"].get("tissue"),
                            "description": samples_dict[sample]["sample"].get("description"),
                            "info": { }
                            }
                        }
        patient_object = {"version": "beacon-individual-v1.0",
                "value": {
                    "id": samples_dict[sample]["patient"].get("id"),
                    "ageOfOnset": samples_dict[sample]["patient"].get("ageOfOnset"),
                    "disease": samples_dict[sample]["patient"].get("disease"),
                    "info": { }
                    }
                }

        variantsFound_object = await create_variantsFound(db_pool, processed_request, samples_dict[sample]["variants"], valid_datasets, include_dataset)

        results.append({"sample": sample_object, "individual": patient_object, "variantsFound": variantsFound_object})


    # We need to restructure the query to create the object that will be shown
    query = create_query(processed_request)

    # Once all this is done, we build the response object
    beacon_response = {
                    "meta": {
                        "Variant": "beacon-variant-v0.1" if not processed_request.get("variant") else processed_request.get("variant"),
  	                    "VariantAnnotation": "beacon-variant-annotation-v1.0" if not processed_request.get("variantAnnotation") else processed_request.get("variantAnnotation"),
                        "VariantMetadata": "beacon-variant-metadata-v1.0" if not processed_request.get("variantMetadata") else processed_request.get("variantMetadata")
                    },
                    "value": { 'beaconId': '.'.join(reversed(request.host.split('.'))),
                        'apiVersion': __apiVersion__,
                        'exists': any([dataset['exists'] for result in results for variant in result["variantsFound"] for dataset in variant["datasetAlleleResponses"]]),
                        'request': { "meta": { "request": { 
                                                            "Sample": "beacon-sample-v1",
                                                            "Variant": "beacon-variant-v0.1" if not processed_request.get("variant") else processed_request.get("variant"),
                                                            "VariantAnnotation": "beacon-variant-annotation-v1.0" if not processed_request.get("variantAnnotation") else processed_request.get("variantAnnotation"),
                                                            "VariantMetadata": "beacon-variant-metadata-v1.0" if not processed_request.get("variantMetadata") else processed_request.get("variantMetadata")
                                                        },
                                                "apiVersion": __apiVersion__,
                                            },
                                    "query": query
                                    },
                        'results': results,
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
    
    return beacon_response






