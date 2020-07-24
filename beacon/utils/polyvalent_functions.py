"""
Functions used by different endpoints. 
 - To do basic operations
 - To parse the filters request
 - To manage access resolution
"""

import ast
import logging
import yaml
import requests
from pathlib import Path

from .. import conf
from .exceptions import BeaconBadRequest, BeaconServerError, BeaconForbidden, BeaconUnauthorised


LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         BASIC FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

def filter_exists(include_dataset, datasets):
    """Return those datasets responses that the `includeDatasetResponses` parameter decides.
    Look at the exist parameter in each returned dataset to established HIT or MISS.
    """
    if include_dataset == 'ALL':
        return datasets
    elif include_dataset == 'NONE':
        return []
    elif include_dataset == 'HIT':
        return [d for d in datasets if d.get('exists') is True]
    elif include_dataset == 'MISS':
        return [d for d in datasets if d.get('exists') is False]


def datasetHandover(dataset_name):
    """Return the datasetHandover with the correct name of the dataset."""
    return [
        { "handoverType" : {
            "id" : "CUSTOM",
            "label" : "Dataset info"
        },
          "note" : "Dataset information and DAC contact details in EGA Website",
          "url" : f"https://ega-archive.org/datasets/{dataset_name}"
        }
    ]


# ----------------------------------------------------------------------------------------------------------------------
#                                         FILTERING TERMS MANAGEMENT
# ----------------------------------------------------------------------------------------------------------------------

def parse_filters_request(filters_request_list):
    """Create a list of the filters passed in the query, where each filter
    is another list in the main list with the following elements: ontology, term, operator, value.
    """

    for unprocessed_filter in filters_request_list:
        ontology, expression = unprocessed_filter.split(":", 1) # DAZ: pray it has ':'
        for operator in [">=", "<=", "=",  ">", "<"]:  # TO DO: raise an error if "=<" or "=>" are given
            if operator in expression:
                term, value = expression.split(operator, 1)
                yield [ontology, term,  operator, value]
                break
        else: # no operator worked
            yield [ontology, expression]


#@capture_server_error('Query filters DB error: ')
async def prepare_filter_parameter(db_pool, filters_request):
    """Parse the filters parameters given in the query to create the string that needs to be passed
    to the SQL query.
    e.g. '(technology)::jsonb ?& array[''Illumina Genome Analyzer II'', ''Illumina HiSeq 2000''] AND 
    (other)::jsonb ?& array[''example1'', ''example2'']
    """

    # First we want to parse the filters request
    if not isinstance(filters_request, list):
        filters_request = ast.literal_eval(filters_request)
        
    list_filters = parse_filters_request(filters_request) # DAZ: I got read of the intermediate list
        
    combinations_list = "','".join([":".join(filter_elements[0:1]) for filter_elements in list_filters])
    combinations_list =  "'" + combinations_list + "'"
    # DAZ: what is that ?

    # Then we connect to the DB and retrieve the parameters that will be passed to the main query
    async with db_pool.acquire(timeout=180) as connection:

        query  = f"""SELECT target_table, column_name, column_value 
                     FROM ontology_term_column_correspondance
                     WHERE concat_ws(':', ontology, term) IN ({combinations_list})"""

        LOG.debug("QUERY filters info: %s", query)
        statement = await connection.prepare(query)
        db_response = await statement.fetch()

        # Organize the responses in a dict with the target_table as keys
        # and as value another dict with column_name as keys and a list of column_value as value
        filter_dict = {}
        for record in db_response:
            target_table = record["target_table"]
            column_name = record["column_name"]
            column_value = str(record["column_value"])
            d = filter_dict.get(target_table, None)
            if d is None:
                d = {}
                filter_dict[target_table] = d
            c = d.get(column_name, None)
            if c is None:
                c = []
                d[column_name] = c
            c.append(column_value)

        # After creating filter_dict, we need to create a list with the SQL strings
        strings_list = []
        final_string = ""
        for target_table, column_name_dict in filter_dict.items():
            if target_table == "public.beacon_dataset_table":
                for column_name, values in column_name_dict.items():
                    string_values = ", ".join(f"'{value}'" for value in values)
                    string = f'({column_name})::jsonb ?& array[{string_values}]'
                    strings_list.append(string)

        # Once we have the different strings, we join them to create the final SQL string
        if not strings_list:
            final_string = 'null'
        else:
            final_string = " AND ".join(strings_list)
        return final_string, filter_dict


# ----------------------------------------------------------------------------------------------------------------------
#                                         ACCESS RELATED FUNCTIONS AND DICT
# ----------------------------------------------------------------------------------------------------------------------

def access_resolution(request, token, host, public_data, registered_data, controlled_data):
    """Determine the access level for a user.

    Depends on user bona_fide_status, and by default it should be PUBLIC.
    """
    permissions = []
    # all should have access to PUBLIC datasets
    # unless the request is for specific datasets
    if public_data:
        permissions.append("PUBLIC")
    access = set(public_data)  # empty if no datasets are given

    # for now we are expecting that the permissions are a list of datasets
    if registered_data and token["bona_fide_status"] is True:
        permissions.append("REGISTERED")
        access = access.union(set(registered_data))
    # if user requests public datasets do not throw an error
    # if both registered and controlled datasets are request this will be shown first
    elif registered_data and not public_data:
        if token["authenticated"] is False:
            # token is not provided (user not authed)
            raise BeaconUnauthorised(request, host, "missing_token", 'Unauthorized access to dataset(s), missing token.')
        # token is present, but is missing perms (user authed but no access)
        raise BeaconForbidden(request, host, 'Access to dataset(s) is forbidden.')
    
    
    token_permissions = token.get('permissions')
    if controlled_data and token_permissions:
        # The idea is to return only accessible datasets

        # Default event, when user doesn't specify dataset ids
        # Contains only dataset ids from token that are present at beacon
        controlled_access = set(controlled_data).intersection(set(token_permissions))
        access = access.union(controlled_access)
        if controlled_access:
            permissions.append("CONTROLLED")
    # if user requests public datasets do not throw an error
    # By default permissions cannot be None, at worst empty set, thus this might never be reached
    elif controlled_data and not (public_data or registered_data):
        if token["authenticated"] is False:
            # token is not provided (user not authed)
            raise BeaconUnauthorised(request, host, "missing_token", 'Unauthorized access to dataset(s), missing token.')
        # token is present, but is missing perms (user authed but no access)
        raise BeaconForbidden(request, host, 'Access to dataset(s) is forbidden.')
    LOG.info(f"Accessible datasets are: {list(access)}.")
    return permissions, list(access)  # DAZ: Maybe no need to convert it


# ----------------------------------------------------------------------------------------------------------------------
#                                    FILTER RESPONSE BASED ON ACCESS LEVELS
# ----------------------------------------------------------------------------------------------------------------------

def filter_response(response, access_levels_dict, accessible_datasets, user_levels, field2access, parent_key=None):
    """
    Recursive function that parses the response of the beacon to filter out those fields that are
    not accessible for the user (based on the access level).

    :response: beacon response
    :access_levels_dict: access levels dictionary created out of the yml file in /utils
    :accessible_datasets: list of datasets accessible by the user (taking into account its privileges)
    :user_levels: list of levels that the user has, i.e ['PUBLIC', 'REGISTERED']
    :field2access: dictionary that maps the child_field name to its corresponding parent_field name in the access levels dict (i.e 'datasets' inside the parent 'beacon' maps to its parent name 'beaconDataset')
    :parent_key: used inside de recursion to store the parent key of the dict we are in
    """
    final_dict = {}
    if isinstance(response, dict):
        for key, val in response.items():
            translated_key = field2access[key] if key in field2access.keys() else key
            specific_access_levels_dict = access_levels_dict[parent_key] if parent_key else access_levels_dict
            if translated_key not in access_levels_dict.keys() and translated_key not in specific_access_levels_dict.keys():
                final_dict[key] = val
            else:
                # if (isinstance(val, dict) or isinstance(val, list)) and key != "info":
                if (isinstance(val, dict) or isinstance(val, list)) and translated_key in access_levels_dict.keys():
                    parent_permission = True
                    self_permission = True if access_levels_dict[translated_key]["accessLevelSummary"] in user_levels else False
                    if parent_key:
                        parent_permission = True if access_levels_dict[parent_key][key] in user_levels else False
                    if self_permission and parent_permission:
                        final_dict[key] = filter_response(val, access_levels_dict, accessible_datasets, user_levels, field2access, translated_key)
                else:
                    valid_level = access_levels_dict[parent_key][translated_key] if parent_key else access_levels_dict[translated_key]
                    if valid_level in user_levels:
                        final_dict[key] = val

    elif isinstance(response, list):
        filtered = []
        for element in response:
            if isinstance(element, dict):
                datasetId = element.get("internalId")
                if not datasetId or datasetId in accessible_datasets:  # controlling specific access permission to show a dataset response
                    filtered.append(filter_response(element, access_levels_dict, accessible_datasets, user_levels, field2access, parent_key))
        return filtered

    return final_dict

# ----------------------------------------------------------------------------------------------------------------------
#                                      VARIANT HANDOVER and extra ANNOTATION
# ----------------------------------------------------------------------------------------------------------------------

def snp_resultsHandover(variantId):
    """Create the resultsHanover dict by inserting the variantId into the template."""

    resultsHandover = [ {
                        "handoverType" : {
                        "id" : "data:1106",
                        "label" : "dbSNP ID"
                        },
                        "note" : "Link to dbSNP database",
                        "url" : f"https://www.ncbi.nlm.nih.gov/snp/?term={variantId}"
                        }, {
                        "handoverType" : {
                        "id" : "data:1106",
                        "label" : "dbSNP ID"
                        },
                        "note" : "Link to dbSNP API",
                        "url" : f"https://api.ncbi.nlm.nih.gov/variation/v0/beta/refsnp/{variantId[2:]}"
                        } ]

    return resultsHandover

async def fetch_variantAnnotations(variant_details):
    """
    Create the a part of the variantsAnnotation response by fetching the cellBase API and the dbSNP API.
    The variant_id has to be in the following format: chrom:start:ref:alt. 
    If in the variantDetails the alt is null, it has to be changed to a '-'.
    """
    
    # cellBase
    chrom = variant_details.get("chromosome", variant_details.get("referenceName"))
    start = variant_details.get("start")
    ref = variant_details.get("referenceBases")
    alt = variant_details.get("alternateBases", '-')

    url = f"http://cellbase.clinbioinfosspa.es/cb/webservices/rest/v4/hsapiens/genomic/variant/{chrom}:{start+1}:{ref}:{alt}/annotation"
    r = requests.get(url)
    cellBase_dict = r.json() if r.status_code == 200 else ''
    try:
        cellBase_rsID = cellBase_dict["response"][0]["result"][0]["id"]
    except KeyError as ke:
        cellBase_rsID = None

    # dbSNP
    variant_id = variant_details.get("variantId")
    rsID = variant_id if variant_id != "." else cellBase_rsID
    if rsID:
        url = f"https://api.ncbi.nlm.nih.gov/variation/v0/beta/refsnp/{rsID[2:]}"
        r = requests.get(url)
        dnSNP_dict = r.json() if r.status_code == 200 else ''
    else:
        dnSNP_dict = ''  # DAZ: eh... a dict ?

    return rsID, cellBase_dict, dnSNP_dict
