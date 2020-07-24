import logging

from aiohttp.web import json_response

from .. import conf
from ..utils.db import patients
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import (Field,
                                 RegexField,
                                 ChoiceField,
                                 IntegerField,
                                 ListField,
                                 DatasetsField)


LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class IndividualsParameters(RequestParameters):
    referenceName = ChoiceField("1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14",
                                "15", "16", "17", "18", "19", "20",
                                "21", "22", "X", "Y", "MT")
    start = IntegerField(min_value=0)
    end = IntegerField(min_value=0)
    startMin = IntegerField(min_value=0)
    startMax = IntegerField(min_value=0)
    endMin = IntegerField(min_value=0)
    endMax = IntegerField(min_value=0)
    referenceBases = RegexField(r'^([ACGTN]+)$')
    alternateBases = RegexField(r'^([ACGTN]+)$')
    assemblyId = RegexField(r'^((GRCh|hg)[0-9]+([.]?p[0-9]+)?)$')
    datasets = DatasetsField()
    biosampleId = Field() # just a text
    filters = ListField(items=RegexField(r'.*:.+=?>?<?[0-9]*$'))
    individualSchemas = ListField(items=ChoiceField("ga4gh-phenopacket-individual-v0.1", "beacon-individual-v0.1"))
    skip = IntegerField(min_value=0, default=0)
    limit = IntegerField(min_value=0, default=10)



# ----------------------------------------------------------------------------------------------------------------------
#                                         UTILITIES
# ----------------------------------------------------------------------------------------------------------------------

## Make lists with the column names that the main SQL function returns
individual_columns = ['individual_stable_id', 'sex', 'ethnicity', 'geographic_origin']
disease_columns = ['disease_id',
                   'disease_age_of_onset_age',
                   'disease_age_of_onset_age_group',
                   'disease_stage',
                   'disease_family_history']
pedigree_columns = ['pedigree_stable_id',
                    'pedigree_role',
                    'pedigree_no_individuals_tested',
                    'pedigree_disease_id']         


def create_query(qparams):
    """
    Restructure the original request to build the query object
    """

    return {
        "variant": {
            "referenceBases": qparams.get("referenceBases", ""),
            "alternateBases": qparams.get("alternateBases", ""),
            "referenceName": qparams.get("referenceName", ""),
            "start": qparams.get("start"),
            "end": qparams.get("end"),
            "assemblyId": qparams.get("assemblyId", "")
        },
        "datasets": {
            "datasetIds": qparams.get("datasets"),
            "includeDatasetResponses": ""
        },
        "filters": qparams.get("filters"),
    }

def create_final_response(qparams_raw, results, alternative_schemas):
    """
    Create the final response as the Beacon Schema expects. 
    """
    alt_schemas_ind = alternative_schemas

    final_response = {
        "meta": {
            "beaconId": conf.beacon_id,
            "apiVersion": conf.api_version,
            "receivedRequest": {
                "meta": {
                    "requestedSchemas": {
                        "individualSchemas": alt_schemas_ind,
                        # REVIEW
                    },
                    "apiVersion": conf.api_version,  # it is hardcoded because we only return v2 for this endpoint
                },
                "query": create_query(qparams_raw),
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
            "beaconHandover": [
                {
                    "handoverType" : {
                        "id" : "CUSTOM",
                        "label" : "Organization contact"
                    },
                    "note" : "Organization contact details maintaining this Beacon",
                    "url" : "mailto:beacon.ega@crg.eu"
                }
            ]
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

def process_response(db_response):
    # Converting the response to a DataFrame 
    response_df = pd.DataFrame([dict(record) for record in db_response]) # do we need the dict?
    # Making sure we don't have NaN values
    response_df = response_df.where(response_df.notnull(), None)
    return True, response_df

# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

proxy = IndividualsParameters()

async def handler(request):
    LOG.info('Running a individuals request')

    qparams_raw, qparams_db = await proxy.fetch(request)
    LOG.debug("Original Query Parameters: %s", qparams_raw)

    # print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy, LOG)

    # 1. GET VALID/ACCESSIBLE DATASETS
    
    # We want to get a list of the datasets available in the database separated in three lists
    # depending on the access level (we check all of them if the user hasn't specified anything, if some
    # there were given, those are the only ones that are checked)
    public_datasets, registered_datasets, controlled_datasets = [], [], []
    for access_type, dataset_id, _ in qparams_db.datasets:
        if access_type == 'PUBLIC':
            public_datasets.append(dataset_id)
        elif access_type == 'REGISTERED':
            registered_datasets.append(dataset_id)
        elif access_type == 'CONTROLLED':
            controlled_datasets.append(dataset_id)

    # 2. REQUEST PROCESSING

    # Add individualId parameter if used
    individual_id = request.match_info.get('target_id_req')

    # 3. RETRIEVE DATA FROM THE DB (use SQL function)

    LOG.info('Connecting to the DB to make the query.')
    exists, response_df = await patients(qparams_db, individual_id, process=process_response)
    LOG.info('Query done.')
    
    # 4. CREATE INDIVIDUALS OBJECT
    LOG.info('Shaping the DB response.')
    alternative_schemas = qparams_raw.get("individualSchemas", [])
    if exists:
        results = create_individuals_object(response_df, alternative_schemas)
    else:
        results = response_df
    LOG.info('Arrangement done.')

    # 5. CREATE FINAL RESPONSE
    LOG.info('Creating the final response.')
    final_response = create_final_response(qparams_raw, results, alternative_schemas)
    LOG.info('Done.')

    return json_response(final_response)
