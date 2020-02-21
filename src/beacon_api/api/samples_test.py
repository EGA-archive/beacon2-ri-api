"""
Samples/Individuals Endpoint.

* ``/samples`` 
* ``/individuals`` 

Query samples/individuals with specific parameters and/or containing a certain variant. 

.. note:: See ``schemas/samples.json`` for checking the parameters accepted in this endpoint.
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
from ..utils.models import variant_object, variantAnnotation_object

from .genomic_query import fetch_resulting_datasets, fetch_variantAnnotations, snp_resultsHandover


LOG = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
#                                         FORMATTING
# ----------------------------------------------------------------------------------------------------------------------

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
    "customFilters": None if not processed_request.get("customFilters") else processed_request.get("customFilters"),
    }

    return query


# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------


# Definition of interesting columns depending on the target object, use for create_individuals_object() and 
# create_samples_object()
sample_columns = ['sample_id', 'sample_stable_id', 'tissue', 'description']
individual_columns = ['patient_id','patient_stable_id', 'sex', 'age_of_onset', 'disease']
variant_columns = ['unique_id', 'dataset_id', 'data_id','chromosome', 'variant_id', 'reference', 
                   'alternate', 'start', 'end', 'type', 'sv_length', 'variant_cnt', 'call_cnt', 
                   'sample_cnt', 'matching_sample_cnt', 'frequency']


def create_individuals_object(main_df):
    by_individual = main_df.groupby('patient_id')

    individual_responses_list = []

    # iterating through the samples and creating the objects
    for individual_id, individual_df in by_individual:
        individual_response = {}

        individual_object = individual_df[individual_columns].drop_duplicates().to_dict('r')[0]
        individual_response['individual'] =  {"version": "beacon-individual-v1.0",
                "value": {
                    "id": individual_object.get("patient_stable_id"),
                    "sex": individual_object.get("sex"),
                    "ageOfOnset": individual_object.get("age_of_onset"),
                    "disease": individual_object.get("disease"),
                    "info": { }
                    }
                }

        samples_object = individual_df[sample_columns].drop_duplicates().to_dict('r')
        individual_response['samples'] = [{"version": "beacon-sample-v1.0",
                        "value": {
                            "id": sample.get("sample_stable_id"),
                            "tissue": sample.get("tissue"),
                            "description": sample.get("description"),
                            "info": { }
                            }
                        }
                        for sample in samples_object]

        variants_raw = individual_df[variant_columns].drop_duplicates().to_dict('r')
        # maybe here we could call the createVariantsFound_object function (or an adapted version)
        individual_response['variantsFound'] = variants_raw
        
        individual_responses_list.append(individual_response)
        
    return individual_responses_list


def create_samples_object(main_df):
    by_sample = main_df.groupby('sample_id')

    sample_responses_list = []

    # iterating through the samples and creating the objects
    for sample_id, sample_df in by_sample:
        sample_response = {}


        sample_object = sample_df[sample_columns].drop_duplicates().to_dict('r')[0]
        sample_response['sample'] = {"version": "beacon-sample-v1.0",
                        "value": {
                            "id": sample_object.get("sample_stable_id"),
                            "tissue": sample_object.get("tissue"),
                            "description": sample_object.get("description"),
                            "info": { }
                            }
                        }

        individuals_object = sample_df[individual_columns].drop_duplicates().to_dict('r')
        sample_response['individuals'] = [{"version": "beacon-individual-v1.0",
                        "value": {
                            "id": individual.get("patient_stable_id"),
                            "sex": individual.get("sex"),
                            "ageOfOnset": individual.get("age_of_onset"),
                            "disease": individual.get("disease"),
                            "info": { }
                            }
                        }
                        for individual in individuals_object]

        variants_raw = sample_df[variant_columns].drop_duplicates().to_dict('r')
        # maybe here we could call the createVariantsFound_object function (or an adapted version)
        sample_response['variantsFound'] = 'variants_raw'

        sample_responses_list.append(sample_response)
        
    return sample_responses_list


async def get_results(db_pool, filters_dict, valid_datasets, processed_request, request):
    """
    Fetches all the data performing a complex query to the DB where all the info about
    samples, variants and individuals can be queried at once. 
    Returns a results object with the 'raw' keys and values. This will have to be shaped
    to match the spec later. 
    """

    # Gathering the variant related parameters passed in the request
    chromosome = '' if not processed_request.get("referenceName") else processed_request.get("referenceName") 
    reference = '' if not processed_request.get("referenceBases") else processed_request.get("referenceBases") 
    alternate = '' if not processed_request.get("alternateBases") else processed_request.get("alternateBases")
    start = 'null' if not processed_request.get("start") else processed_request.get("start")
    end = 'null' if not processed_request.get("end") else processed_request.get("end")
    reference_genome = 'null' if not processed_request.get("assemblyId") else processed_request.get("assemblyId")

    dataset_ids = ",".join([str(i) for i in valid_datasets])

    # Preparing the SQL query with the clauses regarding individuals and samples based on the requests
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
    sentence = 'null' if not sentence_exists else sentence

    # Fetching the info 
    async with db_pool.acquire(timeout=180) as connection:
        try:
            query  = f"""SELECT concat_ws(':', data_t.chromosome, data_t.variant_id, data_t.reference, data_t.alternate, data_t.start, data_t.end, data_t.type) AS unique_id,
                            data_t.dataset_id, vsp_t.data_id, vsp_t.sample_id, vsp_t.patient_id, d_t.reference_genome, data_t.chromosome, data_t.variant_id, data_t.reference, 
                            data_t.alternate, data_t.start, data_t.end, data_t.type, data_t.sv_length, data_t.variant_cnt, data_t.call_cnt, data_t.sample_cnt, data_t.matching_sample_cnt, 
                            data_t.frequency, vsp_t.sample_stable_id, vsp_t.sex, vsp_t.tissue, vsp_t.description, vsp_t.patient_stable_id, vsp_t.age_of_onset, vsp_t.disease
                            FROM public.beacon_data_table as data_t
                            join (select * 
                                    from (SELECT s.id as s_id, s.stable_id as sample_stable_id, s.sex, s.tissue, s.description, 
                                            p.id as patient_id, p.stable_id as patient_stable_id, p.age_of_onset, p.disease 
                                            FROM beacon_sample_table s 
                                            JOIN patient_table p ON s.patient_id = p.id 
                                            -- patient and sample filters
                                            WHERE (CASE WHEN {sentence_exists} THEN {sentence} ELSE true END) AND s.tissue IS NOT NULL) as sample_t
                                    join public.beacon_data_sample_table as data_sample_t
                                    on sample_t.s_id = data_sample_t.sample_id) as vsp_t
                            on data_t.id = vsp_t.data_id
                            join public.beacon_dataset_table as d_t
                            on data_t.dataset_id = d_t.id
                            WHERE 
                            -- dataset filter
                            data_t.dataset_id IN ({dataset_ids}) 
                            -- variant filter
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
                                END)
                            AND (CASE
                                WHEN ('{reference_genome}') IS NOT NULL THEN reference_genome = '{reference_genome}' ELSE true
                                END);"""

            LOG.debug(f"QUERY samples/individuals: {query}")
            statement = await connection.prepare(query)
            db_response = await statement.fetch()

            response = []
            for record in list(db_response):
                response.append(dict(record))
        except Exception as e:
            raise BeaconServerError(f'Query samples/individuals DB error: {e}')
        
        if response: 
            # Converting the response to a DataFrame 
            response_df = pd.DataFrame(response)

            # Calling the functions to create the objects
            # Depending on the endpoint, the function changes
            endpoint = request.path
            LOG.debug(f"Arranging the response for the {endpoint} endpoint.")
            if endpoint == '/individuals_test':
                response_arranged = create_individuals_object(response_df)
            else:
                response_arranged = create_samples_object(response_df)

            # Returning the arrange response
            return response_arranged
        else:
            return []



async def get_valid_datasets(db_pool, dataset_filters):
    """
    Returns a list of the dataset ids that pass the filters
    """
    async with db_pool.acquire(timeout=180) as connection:
        id_list = []
        try: 
            if dataset_filters and dataset_filters != 'null':
                query  = f"""SELECT id
                            FROM beacon_dataset_table
                            WHERE {dataset_filters};"""
            else:
                query  = f"""SELECT id
                            FROM beacon_dataset_table;"""


            LOG.debug(f"QUERY valid datasets: {query}")
            statement = await connection.prepare(query)
            db_response = await statement.fetch()

            for record in list(db_response):
                id_list.append(dict(record).get("id"))

        except Exception as e:
            raise BeaconServerError(f'Query filtered datasets DB error: {e}')

    return id_list


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def sample_request_handler_test(db_pool, processed_request, request):
    """
    Execute query with SQL function.
    """

    # First we are going to get the lists of the available datasets
    public_datasets, registered_datasets, controlled_datasets = await fetch_datasets_access(db_pool, processed_request.get("datasetIds"))

        ##### TEST
        # access_type, accessible_datasets = access_resolution(request, request['token'], request.host, public_datasets, registered_datasets, controlled_datasets)
        # LOG.info(f"The user has this types of access: {access_type}")
        # query_parameters[-2] = ",".join([str(id) for id in accessible_datasets])
        ##### END TEST

    # NOTICE that right now we will just focus on the PUBLIC ones to ease the process, so we get all their ids and add them to the query
    available_datasets = public_datasets

    # We will output the datasets depending on the includeDatasetResponses parameter
    include_dataset = ""
    if processed_request.get("includeDatasetResponses"):
        include_dataset  = processed_request.get("includeDatasetResponses")
    else:
        include_dataset  = "ALL"

    # Then we are going to parse the filters to separate them depending on their target table
    filters_list = [] if not processed_request.get("filters") else processed_request.get("filters")
    custom_filters_list = [] if not processed_request.get("customFilters") else processed_request.get("customFilters")
    if filters_list or custom_filters_list:
        all_filters_list = filters_list + custom_filters_list
        dataset_filters, filters_dict = await prepare_filter_parameter(db_pool, all_filters_list)
    else:
        dataset_filters = ""
        filters_dict = {}
        

    # we'll need to apply the dataset related filters (if there is any) so we are going to generate a list
    # with the ones that pass the dataset_filters filters
    valid_datasets = await  get_valid_datasets(db_pool, dataset_filters)

    # The intersection between the datasets that are available by access and the datasets that have passed the filters
    # is the final list of valid_datasets
    valid_datasets = [dataset for dataset in valid_datasets if dataset in available_datasets]

    # Now we perform the main query to the DB to retrieve all the sample, individual and variant raw data
    results = await get_results(db_pool, filters_dict, valid_datasets, processed_request, request)

            
    # In the response only a subset of variants will be shown, except when includeAllVariants is set to true
    # if that's not the case, we are going to create an object to facilitate the link for getting all of them
    all_variants_url = { "info": "For optimization reasons, only a subset of variants are shown for each sample. If you would like to get all of them, visit the link below.",
                        "url": f"https://testv2-beacon-api.ega-archive.org{request.rel_url}&includeAllVariants=true"
                        }

    # We need to restructure the query to create the object that will be shown
    query = create_query(processed_request)

    # Make lists of the models requests to show it in the response
    variant = processed_request.get("variant").split(",") if processed_request.get("variant") else []
    variantAnnotation = processed_request.get("variantAnnotation").split(",") if processed_request.get("variantAnnotation") else [] 
    variantMetadata = processed_request.get("variantMetadata").split(",") if processed_request.get("variantMetadata") else [] 

    # Once all this is done, we build the response object
    beacon_response = {
                    "meta": {
                        "Variant": ["beacon-variant-v0.1", "ga4gh-variant-representation-v0.1"],
  	                    "VariantAnnotation": ["beacon-variant-annotation-v1.0"],
                        "VariantMetadata": ["beacon-variant-metadata-v1.0"]
                    },
                    "value": { 'beaconId': __id__,
                        'apiVersion': __apiVersion__,
                        'exists': '',
                        # 'exists': any([dataset['exists'] for result in results for variant in result["variantsFound"] for dataset in variant["datasetAlleleResponses"]]),
                        'request': { "meta": { "request": { 
                                                            "Sample": "beacon-sample-v1",
                                                            "Variant": ["beacon-variant-v0.1"]  + variant,
                                                            "VariantAnnotation": ["beacon-variant-annotation-v1.0"] + variantAnnotation,
                                                            "VariantMetadata": ["beacon-variant-metadata-v1.0"] + variantMetadata
                                                        },
                                                "apiVersion": __apiVersion__,
                                            },
                                    "query": query
                                    },
                        'results': results,
                        'info': None,
                        'resultsHandover': None if processed_request.get("includeAllVariants") == "true" else all_variants_url,
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
