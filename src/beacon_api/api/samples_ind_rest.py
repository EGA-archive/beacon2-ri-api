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

from ..utils.polyvalent_functions import (create_prepstmt_variables,
                                          filter_exists,
                                          datasetHandover,
                                          prepare_filter_parameter,
                                          fetch_datasets_access,
                                          access_resolution)
from ..utils.models import variant_object, variantAnnotation_object, biosample_object, individual_object

from .genomic_query import fetch_resulting_datasets, fetch_variantAnnotations, snp_resultsHandover
from .samples_ind import get_results_simple, create_variantsFound_object, get_valid_datasets, create_query
from .samples_ind import sample_columns, individual_columns, variant_columns, dataset_columns, variant_and_dataset_columns, disease_columns, pedigree_columns

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

# We will reuse a lot of functions and objects from .samples_ind.py
# The ones that have to be slightly modified to fit these endpoints will be here

async def create_smt_object(db_pool, main_df, include_dataset, processed_request, valid_datasets, target_query):
    
    responses_list = []

    # choosing the parsing based on the target_query
    if target_query == 'samples':
        samples_object = main_df[sample_columns].drop_duplicates().to_dict('r')
        responses_list = [biosample_object(sample, processed_request) for sample in samples_object]

    elif target_query == 'individuals':
        by_individual = main_df.groupby('patient_id')
        for _, individual_df in by_individual:
            individual = individual_df[individual_columns].drop_duplicates().to_dict('r')[0]
            # adding the info about diseases and pedigrees
            diseases = individual_df[disease_columns].drop_duplicates().to_dict('r')
            individual.update({'diseases': diseases})
            pedigrees = individual_df[pedigree_columns].drop_duplicates().to_dict('r')
            individual.update({'pedigrees': pedigrees})

            responses_list.append(individual_object(individual, processed_request))

    elif target_query == 'variants':
        variants_df = main_df[variant_and_dataset_columns].drop_duplicates()
        responses_list = await create_variantsFound_object(db_pool, variants_df, include_dataset, processed_request, valid_datasets)
        
    return responses_list



async def get_results_smt(db_pool, filters_dict, valid_datasets, processed_request, request, include_dataset): 
    """
    Fetches all the data performing a complex query to the DB where all the info about
    samples, variants and individuals can be queried at once. 
    Returns a results object with the 'raw' keys and values. This will have to be shaped
    to match the spec later. 
    """
    # Parsing the request to get the target_element, target_sample_id/target_individual_id and the target_query
    target_element = request.path[1:].split("/")[0]
    target_query = request.path[1:].split("/")[2]

    target_sample_id = ''
    target_individual_id = ''
    if target_element == "individuals":
        target_individual_id = request.match_info['target_id_req']
    elif target_element == "samples":
        target_sample_id = request.match_info['target_id_req']

    # Gathering the variant related parameters MAYBE passed in the request
    chromosome = '' if not processed_request.get("referenceName") else processed_request.get("referenceName") 
    reference = '' if not processed_request.get("referenceBases") else processed_request.get("referenceBases") 
    alternate = '' if not processed_request.get("alternateBases") else processed_request.get("alternateBases")
    start = 'null' if not processed_request.get("start") else processed_request.get("start")
    end = 'null' if not processed_request.get("end") else processed_request.get("end")
    reference_genome = '' if not processed_request.get("assemblyId") else processed_request.get("assemblyId")

    dataset_ids = ",".join([str(i) for i in valid_datasets])

    # Preparing the SQL query with the clauses regarding individuals and samples based on the requests
    sentence = []
    target_table_sample = f"{DB_SCHEMA}.beacon_sample_table"
    target_table_patient = f"{DB_SCHEMA}.patient_table"
    samples_filter_dict = None if not filters_dict.get(target_table_sample) else filters_dict.get(target_table_sample)
    patients_filter_dict = None if not filters_dict.get(target_table_patient) else filters_dict.get(target_table_patient)

    # Update the patients_filter_dict with disease and pedigree info
    target_table_patient_disease = f"{DB_SCHEMA}.patient_disease_table"
    if filters_dict.get(target_table_patient_disease):
        patients_filter_dict.update(filters_dict.get(target_table_patient_disease))

    target_table_patient_pedigree = f"{DB_SCHEMA}.patient_pedigree_table"
    if filters_dict.get(target_table_patient_pedigree):
        patients_filter_dict.update(filters_dict.get(target_table_patient_pedigree))

    # Join everything in an SQL-friendly format
    # Notice we are also taking into account the target element for deciding which filters we use
    if samples_filter_dict and target_element == "individuals":
        for column, list_values in samples_filter_dict.items():
            sentence_part = f""" s.{column} IN ('{"','".join(list_values)}')"""
            sentence.append(sentence_part)
    if patients_filter_dict and target_element == "samples":
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
                            data_t.dataset_id, d_t.reference_genome, d_t.stable_id as stable_id_dt, d_t.access_type, vsp_t.data_id, data_t.chromosome, data_t.variant_id, 
                            data_t.reference, data_t.alternate, data_t.start, data_t.end, data_t.type, data_t.sv_length, data_t.variant_cnt, data_t.call_cnt, data_t.sample_cnt, 
                            data_t.matching_sample_cnt, data_t.frequency, vsp_t.sample_id, vsp_t.sample_stable_id, vsp_t.description, vsp_t.biosample_status, 
							vsp_t.individual_age_at_collection_age, vsp_t.individual_age_at_collection_age_group, vsp_t.organ, vsp_t.tissue, vsp_t.cell_type, 
							vsp_t.obtention_procedure, vsp_t.tumor_progression, vsp_t.tumor_grade,
							vsp_t.patient_id, vsp_t.patient_stable_id, 
                            vsp_t.sex, vsp_t.ethnicity, vsp_t.geographic_origin,
							-- patient_disease_table
							vsp_t.disease, vsp_t.age, vsp_t.age_group, vsp_t.stage, vsp_t.family_history,
							-- patient_pedigree_table
							vsp_t.pedigree_id, vsp_t.pedigree_role, vsp_t.number_of_individuals_tested, vsp_t.pedigree_disease, vsp_t.pedigree_description
                            FROM public.beacon_data_table as data_t
                            join (select * 
                                    from (SELECT s.id as s_id, s.stable_id as sample_stable_id, s.description, 
										  	s.biosample_status, s.individual_age_at_collection_age, s.individual_age_at_collection_age_group, 
										  	s.organ, s.tissue, s.cell_type, s.obtention_procedure, s.tumor_progression, s.tumor_grade,
                                            p.*
                                            FROM beacon_sample_table s 
                                            JOIN (SELECT p.id as patient_id, p.stable_id as patient_stable_id, p.sex, p.ethnicity, 
													p.geographic_origin,
													-- patient_disease_table
													pd.disease, pd.age, pd.age_group, pd.stage, pd.family_history,
													-- patient_pedigree_table
													pp.pedigree_id, pp.pedigree_role, pp.number_of_individuals_tested, pp.pedigree_disease, pp.pedigree_description
															FROM patient_table p 
															-- patient_disease_table
															LEFT JOIN patient_disease_table as pd
															ON p.id = pd.patient_id
															-- patient_pedigree_table
															LEFT JOIN (SELECT patient_id, pedigree_id, pedigree_role, number_of_individuals_tested, 
																	   disease as pedigree_disease, pedigree_table.description as pedigree_description
																		FROM patient_pedigree_table
																		JOIN pedigree_table
																		ON pedigree_id = id) as pp
															ON p.id = pp.patient_id) as p 
										  	ON s.patient_id = p.patient_id
                                            -- patient and sample filters
                                            ---- generals
                                            WHERE (CASE WHEN {sentence_exists} THEN {sentence} ELSE true END) AND s.tissue IS NOT NULL
                                            ---- by ID
                                            AND (CASE WHEN nullif('{target_sample_id}', '') IS NOT NULL THEN s.stable_id = '{target_sample_id}' ELSE true END)
                                            AND (CASE WHEN nullif('{target_individual_id}', '') IS NOT NULL THEN patient_stable_id = '{target_individual_id}' ELSE true END)
                                            ) as sample_t
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
                                WHEN nullif('{reference_genome}', '') IS NOT NULL THEN reference_genome = '{reference_genome}' ELSE true
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
            # Making sure we don't have NaN values
            response_df = response_df.where(response_df.notnull(), None)

            # Calling the functions to create the objects
            # Depending on the target_query, we pass a different parameter to the function
            LOG.debug(f"Arranging the response for the {target_query} query.")

            response_arranged = await create_smt_object(db_pool, response_df, include_dataset, processed_request, valid_datasets, target_query)

            LOG.debug(f"Arrangement done for the {target_query} query.")
            # Returning the arrange response
            return response_arranged
        else:
            LOG.debug(f"No response for this query on the {endpoint} endpoint.")
            return []



# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

#######################
#######  BY ID ########
#######################

async def by_id_handler(db_pool, request, processed_request):
    """
    """

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


    # In this case, the query field will be empty
    query = []

    # Make lists of the models requests to show it in the response
    variant = processed_request.get("variant").split(",") if processed_request.get("variant") else []
    variantAnnotation = processed_request.get("variantAnnotation").split(",") if processed_request.get("variantAnnotation") else [] 
    variantMetadata = processed_request.get("variantMetadata").split(",") if processed_request.get("variantMetadata") else [] 
    biosample = processed_request.get("biosample").split(",") if processed_request.get("biosample") else [] 
    individual = processed_request.get("individual").split(",") if processed_request.get("individual") else [] 

    # Once all this is done, we build the response object
    beacon_response = {
                    "meta": {
                        "Variant": ["beacon-variant-v0.1", "ga4gh-variant-representation-v0.1"],
  	                    "VariantAnnotation": ["beacon-variant-annotation-v1.0"],
                        "VariantMetadata": ["beacon-variant-metadata-v1.0"],
                        "biosample": ["beacon-biosample-v0.1", "ga4gh-phenopacket-biosample-v0.1"],
                        "individual": ["beacon-individual-v0.1", "ga4gh-phenopacket-individual-v0.1"],
                    },
                    "value": { 'beaconId': __id__,
                        'apiVersion': __apiVersion__,
                        'exists': any(results),
                        # 'exists': any([dataset['exists'] for result in results for variant in result["variantsFound"] for dataset in variant["datasetAlleleResponses"]]),
                        'request': { "meta": { "request": { 
                                                            "Variant": ["beacon-variant-v0.1"]  + variant,
                                                            "VariantAnnotation": ["beacon-variant-annotation-v1.0"] + variantAnnotation,
                                                            "VariantMetadata": ["beacon-variant-metadata-v1.0"] + variantMetadata,
                                                            "sample": ["beacon-biosample-v0.1"] + biosample,
                                                            "individual": ["beacon-individual-v0.1"] + individual
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


#######################
###### ID + SMT #######
#######################

async def smt_by_id(db_pool, processed_request, request):
    """
    Function that handles the endpoints of type: smt/{id}/smt
    It is based on the pipeline done in .samples_ind.py
    """

    # First we are going to get the lists of the available datasets
    public_datasets, registered_datasets, controlled_datasets = await fetch_datasets_access(db_pool, str(processed_request.get("datasetIds")))

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

    # Now we perform the main query to the DB to retrieve all the sample, individual or variant  data
    results = await get_results_smt(db_pool, filters_dict, valid_datasets, processed_request, request, include_dataset)

    # We need to restructure the query to create the object that will be shown
    query = create_query(processed_request)

    # Make lists of the models requests to show it in the response
    variant = processed_request.get("variant").split(",") if processed_request.get("variant") else []
    variantAnnotation = processed_request.get("variantAnnotation").split(",") if processed_request.get("variantAnnotation") else [] 
    variantMetadata = processed_request.get("variantMetadata").split(",") if processed_request.get("variantMetadata") else [] 
    biosample = processed_request.get("biosample").split(",") if processed_request.get("biosample") else [] 
    individual = processed_request.get("individual").split(",") if processed_request.get("individual") else [] 

    # Once all this is done, we build the response object
    beacon_response = {
                    "meta": {
                        "Variant": ["beacon-variant-v0.1", "ga4gh-variant-representation-v0.1"],
  	                    "VariantAnnotation": ["beacon-variant-annotation-v1.0"],
                        "VariantMetadata": ["beacon-variant-metadata-v1.0"],
                        "biosample": ["beacon-biosample-v0.1", "ga4gh-phenopacket-biosample-v0.1"],
                        "individual": ["beacon-individual-v0.1", "ga4gh-phenopacket-individual-v0.1"],
                    },
                    "value": { 'beaconId': __id__,
                        'apiVersion': __apiVersion__,
                        'exists': any(results),
                        # 'exists': any([dataset['exists'] for result in results for variant in result["variantsFound"] for dataset in variant["datasetAlleleResponses"]]),
                        'request': { "meta": { "request": { 
                                                            "Variant": ["beacon-variant-v0.1"]  + variant,
                                                            "VariantAnnotation": ["beacon-variant-annotation-v1.0"] + variantAnnotation,
                                                            "VariantMetadata": ["beacon-variant-metadata-v1.0"] + variantMetadata,
                                                            "sample": ["beacon-biosample-v0.1"] + biosample,
                                                            "individual": ["beacon-individual-v0.1"] + individual
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
