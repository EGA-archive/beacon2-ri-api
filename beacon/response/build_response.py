from typing import Optional
import subprocess
from beacon import conf
from beacon.db.schemas import DefaultSchemas
from beacon.request import RequestParams
from beacon.request.model import Granularity
from beacon.db.datasets import beacon_handovers, beacon_handovers_by_dataset

import logging

LOG = logging.getLogger(__name__)

def build_meta(qparams: RequestParams, entity_schema: Optional[DefaultSchemas], returned_granularity: Granularity):
    """"Builds the `meta` part of the response

    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """
    try:
        meta = {
            'beaconId': conf.beacon_id,
            'apiVersion': conf.api_version,
            'returnedGranularity': returned_granularity,
            'receivedRequestSummary': qparams.summary(),
            'returnedSchemas': [entity_schema.value] if entity_schema is not None else []
        }
    except Exception:
        meta = {
            'beaconId': conf.beacon_id,
            'apiVersion': conf.api_version,
            'returnedGranularity': returned_granularity,
            'receivedRequestSummary': qparams,
            'returnedSchemas': [entity_schema.value] if entity_schema is not None else []
        }
    return meta

def build_response_summary(exists, num_total_results):
    LOG.debug(num_total_results)
    if num_total_results is None:
        return {
            'exists': exists
        }
    else:
        return {
            'exists': exists,
            'numTotalResults': num_total_results
        }


def build_response_summary_by_dataset(exists, num_total_results, data):
    #LOG.debug(data)
    count=num_total_results
    LOG.debug(count)
    if count == 0:
        return {
            'exists': count > 0
        }
    else:
        return {
            'exists': count > 0,
            'numTotalResults': count
        }


def build_response_by_dataset(data, dict_counts, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""
    list_of_responses=[]
    for k,v in data.items():

        if v:
            response = {
                'id': k, # TODO: Set the name of the dataset/cohort
                'setType': 'dataset', # TODO: Set the type of collection
                'exists': dict_counts[k] > 0,
                'resultsCount': dict_counts[k],
                'results': v,
                # 'info': None,
                'resultsHandover': beacon_handovers_by_dataset(k),  # build_results_handover
            }
            
            list_of_responses.append(response)
            LOG.debug(list_of_responses)
            

    #LOG.debug(list_of_responses)
    return list_of_responses

def build_response(data, num_total_results, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""
    limit = qparams.query.pagination.limit
    include = qparams.query.include_resultset_responses
    if include == 'NONE':
            response = {
            'id': '', # TODO: Set the name of the dataset/cohort
            'setType': '', # TODO: Set the type of collection
            'exists': num_total_results > 0,
            'resultsCount': num_total_results,
            'results': data,
            # 'info': None,
            'resultsHandover': beacon_handovers(),  # build_results_handover
        }
    elif limit != 0 and limit < num_total_results:
        response = {
            'id': '', # TODO: Set the name of the dataset/cohort
            'setType': '', # TODO: Set the type of collection
            'exists': num_total_results > 0,
            'resultsCount': limit,
            'results': data,
            # 'info': None,
            'resultsHandover': beacon_handovers(),  # build_results_handover
        }
    else:
        response = {
            'id': '', # TODO: Set the name of the dataset/cohort
            'setType': '', # TODO: Set the type of collection
            'exists': num_total_results > 0,
            'resultsCount': num_total_results,
            'results': data,
            # 'info': None,
            'resultsHandover': beacon_handovers(),  # build_results_handover
        }

    return response


########################################
# Resultset Response
########################################
def build_beacon_resultset_response(data,
                                    num_total_results,
                                    qparams: RequestParams,
                                    func_response_type,
                                    entity_schema: DefaultSchemas):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'response': {
            'resultSets': [build_response(data, num_total_results, qparams, func_response_type)]
        },
        'beaconHandovers': beacon_handovers(),
    }
    return beacon_response

def build_beacon_resultset_response_by_dataset(data,
                                    dict_counts,
                                    num_total_results,
                                    qparams: RequestParams,
                                    func_response_type,
                                    entity_schema: DefaultSchemas):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary_by_dataset(num_total_results > 0, num_total_results, data),
        # TODO: 'extendedInfo': build_extended_info(),
        'response': {
            'resultSets': build_response_by_dataset(data, dict_counts, qparams, func_response_type)
        },
        'beaconHandovers': beacon_handovers(),
    }
    #LOG.debug(beacon_response)
    return beacon_response

########################################
# Count Response
########################################

def build_beacon_count_response(data,
                                    num_total_results,
                                    qparams: RequestParams,
                                    func_response_type,
                                    entity_schema: DefaultSchemas):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.COUNT),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'beaconHandovers': beacon_handovers(),
    }
    return beacon_response

########################################
# Boolean Response
########################################

def build_beacon_boolean_response(data,
                                    num_total_results,
                                    qparams: RequestParams,
                                    func_response_type,
                                    entity_schema: DefaultSchemas):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.BOOLEAN),
        'responseSummary': build_response_summary(num_total_results > 0, None),
        # TODO: 'extendedInfo': build_extended_info(),
        'beaconHandovers': beacon_handovers(),
    }
    return beacon_response

########################################
# Collection Response
########################################

def build_beacon_collection_response(data, num_total_results, qparams: RequestParams, func_response_type, entity_schema: DefaultSchemas):
    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'info': build_extended_info(),
        'beaconHandovers': beacon_handovers(),
        'response': {
            'collections': func_response_type(data, qparams)
        }
    }
    return beacon_response

########################################
# Info Response
########################################

def build_beacon_info_response(data, qparams, func_response_type, authorized_datasets=None):
    if authorized_datasets is None:
        authorized_datasets = []

    beacon_response = {
        'meta': build_meta(qparams, None, Granularity.RECORD),
        'response': {
            'id': conf.beacon_id,
            'name': conf.beacon_name,
            'apiVersion': conf.api_version,
            'environment': conf.environment,
            'organization': {
                'id': conf.org_id,
                'name': conf.org_name,
                'description': conf.org_description,
                'address': conf.org_adress,
                'welcomeUrl': conf.org_welcome_url,
                'contactUrl': conf.org_contact_url,
                'logoUrl': conf.org_logo_url,
            },
            'description': conf.description,
            'version': conf.version,
            'welcomeUrl': conf.welcome_url,
            'alternativeUrl': conf.alternative_url,
            'createDateTime': conf.create_datetime,
            'updateDateTime': conf.update_datetime,
            'datasets': func_response_type(data, qparams, authorized_datasets),
        }
    }

    return beacon_response

########################################
# Error Response
########################################

def build_beacon_error_response(errorCode, qparams, errorMessage):

    beacon_response = {
        'meta': build_meta(qparams, None, Granularity.RECORD),
        'error': {
            'errorCode': str(errorCode),
            'errorMessage': str(errorMessage)
        }
    }

    return beacon_response

########################################
# Service Info Response
########################################

def build_beacon_service_info_response():
    beacon_response = {
        'id': conf.beacon_id,
        'name': conf.beacon_name,
        'type': {
            'group': conf.ga4gh_service_type_group,
            'artifact': conf.ga4gh_service_type_artifact,
            'version': conf.ga4gh_service_type_version
        },
        'description': conf.description,
        'organization': {
            'name': conf.org_name,
            'url': conf.org_welcome_url
        },
        'contactUrl': conf.org_contact_url,
        'documentationUrl': conf.documentation_url,
        'createdAt': conf.create_datetime,
        'updatedAt': conf.update_datetime,
        'environment': conf.environment,
        'version': conf.version,
    }

    return beacon_response

########################################
# Filtering terms Response
########################################

def build_filtering_terms_response(data,
                                    num_total_results,
                                    qparams: RequestParams,
                                    func_response_type,
                                    entity_schema: DefaultSchemas):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'response': {
            'filteringTerms': data,
            'resources': [{"id": "hp","name": "Human Phenotype Ontology","url": "https://purl.obolibrary.org/obo/hp.owl","version": "27-03-2020","namespacePrefix": "HP","iriPrefix": "https://purl.obolibrary.org/obo/HP_"},
                {"id": "icd10","name": "International Classification of Diseaes 10th edition","version": "17-03-2008","namespacePrefix": "ICD10"},
                {"id": "ncit","name": "National Cancer Institute Thesaurus","url": "https://purl.obolibrary.org/obo/ncit.owl","version": "19-10-2023","namespacePrefix": "NCIT","iriPrefix": "https://purl.obolibrary.org/obo/NCIT_"},
                {"id": "loinc","name": "Logical Observation Identifiers Names and Codes","url": "https://loinc.org/download/loinc-complete/","version": "19-10-2023","namespacePrefix": "LOINC"},
                {"id": "gaz","name": "Gazetteer","url": "https://purl.obolibrary.org/obo/gaz.owl","namespacePrefix": "GAZ","iriPrefix": "https://purl.obolibrary.org/obo/GAZ_"},
                {"id": "opcs4","name": "Office of Population Censuses and Surveys 4th revision","version": "01-04-2023","namespacePrefix": "OPCS4"},
                {"id": "genepio","name": "Genomic Epidemiology Ontology","version": "19-08-2023","namespacePrefix": "GENEPIO"},
                {"id": "obi","name": "Ontology for Biomedical Investigations","url": "http://purl.obolibrary.org/obo/obi.owl","version": "19-01-2024","namespacePrefix": "OBI","iriPrefix": "https://purl.obolibrary.org/obo/OBI_"},
                {"id": "efo","name": "Experimental Factor Ontology","version": "15-04-2024","namespacePrefix": "EFO"},
                {"id": "uberon","name": "Uber-anatomy ontology","version": "22-03-2024","namespacePrefix": "UBERON"},
                {"id": "doid","name": "Human Disease Ontology","url": "http://purl.obolibrary.org/obo/doid.owl","version": "28-03-2024","namespacePrefix": "DOID","iriPrefix": "https://purl.obolibrary.org/obo/DOID_"},
                {"id": "geno","name": "GENO ontology","version": "08-10-2023","namespacePrefix": "GENO"}]
        },
        'beaconHandovers': beacon_handovers(),
    }
    return beacon_response

