"""
Functions used by different endopoints. 
 - To do basic operations
 - To parse the filters request
 - To manage access resolution
"""

import ast
import logging
import yaml
import requests
from pathlib import Path

from ..api.exceptions import BeaconBadRequest, BeaconServerError, BeaconForbidden, BeaconUnauthorised
from .. import __apiVersion__
from ..conf.config import DB_SCHEMA

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         BASIC FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

def create_prepstmt_variables(value):
    """Takes a value of how many prepared variables you want to pass a query
    and creates a string to put it in it"""
    dollars = []
    for element in range(value):
        element += 1
        variable = "$" + str(element)
        dollars.append(variable)

    return ", ".join(dollars)



def filter_exists(include_dataset, datasets):
    """Return those datasets responses that the `includeDatasetResponses` parameter decides.
    Look at the exist parameter in each returned dataset to established HIT or MISS.
    """
    if include_dataset == 'ALL':
        return datasets
    elif include_dataset == 'NONE':
        return []
    elif include_dataset == 'HIT':
        return [d for d in datasets if d['exists'] is True]
    elif include_dataset == 'MISS':
        return [d for d in datasets if d['exists'] is False]


def datasetHandover(dataset_name):
    """Return the datasetHandover with the correct name of the dataset."""
    datasetHandover = [ { "handoverType" : {
                                        "id" : "CUSTOM",
                                        "label" : "Dataset info"
                                    },
                                    "note" : "Dataset information and DAC contact details in EGA Website",
                                    "url" : f"https://ega-archive.org/datasets/{dataset_name}"
                                    } ]
    return datasetHandover


# ----------------------------------------------------------------------------------------------------------------------
#                                         YAML LOADER
# ----------------------------------------------------------------------------------------------------------------------

def find_yml_and_load(input_file):
    """Try to load the access levels yaml and return it as a dict."""
    file = Path(input_file)

    if not file.exists():
        LOG.error(f"The file '{file}' does not exist", file=sys.stderr)
        return

    if file.suffix in ('.yaml', '.yml'):
        with open(file, 'r') as stream:
            file_dict = yaml.safe_load(stream)
            return file_dict

    # Otherwise, fail
    LOG.error(f"Unsupported format for {file}", file=sys.stderr)


# ----------------------------------------------------------------------------------------------------------------------
#                                         FILTERING TERMS MANAGEMENT
# ----------------------------------------------------------------------------------------------------------------------

def parse_filters_request(filters_request_list):
    """Create a list of the filters passed in the query, where each filter
    is another list in the main list with the following elements: ontology, term, operator, value.
    """
    list_filters = []
    for unprocessed_filter in filters_request_list:
        filter_elements = unprocessed_filter.split(":")
        ontology = filter_elements[0]
        operator_switch = False
        for operator in [">=", "<=", "=",  ">", "<"]:  # TO DO: raise an error if "=<" or "=>" are given
            if operator in filter_elements[1]:
                operator = operator
                term = filter_elements[1].split(operator)[0]
                value = filter_elements[1].split(operator)[1]
                operator_switch = True
                break

        if operator_switch:
            final_elements = [ontology, term,  operator, value]
            operator_switch = False
        else:
            final_elements = [ontology, filter_elements[1]]

        list_filters.append(final_elements)

    return list_filters


async def prepare_filter_parameter(db_pool, filters_request):
    """Parse the filters parameters given in the query to create the string that needs to be passed
    to the SQL query.
    e.g. '(technology)::jsonb ?& array[''Illumina Genome Analyzer II'', ''Illumina HiSeq 2000''] AND 
    (other)::jsonb ?& array[''example1'', ''example2'']
    """

    # First we want to parse the filters request
    if isinstance(filters_request, list):
        list_filters = parse_filters_request(filters_request)
    else:
        list_filters = parse_filters_request(ast.literal_eval(filters_request))
        
    combinations_list = "','".join([":".join([filter_elements[0],filter_elements[1]]) for filter_elements in list_filters])
    combinations_list =  "'" + combinations_list + "'"

    # Then we connect to the DB and retrieve the parameters that will be passed to the main query
    async with db_pool.acquire(timeout=180) as connection:

        try: 
            query  = f"""SELECT target_table, column_name, column_value 
                        FROM ontology_term_column_correspondance
                        WHERE concat_ws(':', ontology, term) IN ({combinations_list})"""

            LOG.debug(f"QUERY filters info: {query}")
            statement = await connection.prepare(query)
            db_response = await statement.fetch()

            filter_dict = {}
            for record in list(db_response):
                if record["target_table"] not in filter_dict.keys():
                    filter_dict[record["target_table"]] = {}
                    filter_dict[record["target_table"]][record["column_name"]] = []
                    filter_dict[record["target_table"]][record["column_name"]].append(record["column_value"])
                elif record["column_name"] not in filter_dict[record["target_table"]].keys():
                    filter_dict[record["target_table"]][record["column_name"]] = []
                    filter_dict[record["target_table"]][record["column_name"]].append(record["column_value"])
                else:
                    filter_dict[record["target_table"]][record["column_name"]].append(record["column_value"])

            # After we have retrieved the values in a dict with the target_table as keys and as value another dict with column_name as keys, we need to create the final string
            strings_list = []
            final_string = ""
            for target_table, column_name_dict in filter_dict.items():
                if target_table == "public.beacon_dataset_table":
                    for column_name, values in column_name_dict.items():
                        string_values = ", ".join("'" + str(value) + "'" for value in values)
                        string = f'({column_name})::jsonb ?& array[{string_values}]'
                        strings_list.append(string)

            # Once we have the response, we parse it to create the final string needed as input
            if not strings_list:
                final_string = 'null'
            else:
                final_string = " AND ".join(strings_list)
            return str(final_string), filter_dict

        except Exception as e:
               raise BeaconServerError(f'Query filters DB error: {e}') 


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
    
    
    if controlled_data and 'permissions' in token and token['permissions']:
        # The idea is to return only accessible datasets

        # Default event, when user doesn't specify dataset ids
        # Contains only dataset ids from token that are present at beacon
        controlled_access = set(controlled_data).intersection(set(token['permissions']))
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
    LOG.info(f"Accesible datasets are: {list(access)}.")
    return permissions, list(access)


async def fetch_datasets_access(db_pool, datasets):
    """Retrieve 3 list of the available datasets depending on the access type"""
    LOG.info('Retrieving info about the available datasets (id and access type).')
    public = []
    registered = []
    controlled = []
    async with db_pool.acquire(timeout=180) as connection:
        async with connection.transaction():
            datasets_query = None if datasets == "null" or not datasets else ast.literal_eval(datasets)
            try:
                query = f"""SELECT access_type, id, stable_id FROM {DB_SCHEMA}.beacon_dataset
                           WHERE coalesce(stable_id = any($1), true);
                           """
                LOG.debug(f"QUERY datasets access: {query}")
                statement = await connection.prepare(query)
                db_response = await statement.fetch(datasets_query)
                for record in list(db_response):
                    if record['access_type'] == 'PUBLIC':
                        public.append(record['id'])
                    if record['access_type'] == 'REGISTERED':
                        registered.append(record['id'])
                    if record['access_type'] == 'CONTROLLED':
                        controlled.append(record['id'])
                return public, registered, controlled
            except Exception as e:
                raise BeaconServerError(f'Query available datasets DB error: {e}')

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
    chrom = variant_details.get("chromosome") if variant_details.get("chromosome") else variant_details.get("referenceName")
    start = variant_details.get("start")
    ref = variant_details.get("referenceBases")
    alt = variant_details.get("alternateBases") if variant_details.get("alternateBases") else '-'

    variant_id = ":".join([str(chrom), str(start + 1), ref, alt])
    url = f"http://cellbase.clinbioinfosspa.es/cb/webservices/rest/v4/hsapiens/genomic/variant/{variant_id}/annotation"
    r = requests.get(url)
    cellBase_dict = r.json() if r else ''
    try:
        cellBase_rsID = cellBase_dict["response"][0]["result"][0]["id"]
    except:
        cellBase_rsID = None

    # dbSNP
    rsID = variant_details.get("variantId") if (variant_details.get("variantId") and variant_details.get("variantId") != ".") else cellBase_rsID
    if rsID:
        url = f"https://api.ncbi.nlm.nih.gov/variation/v0/beta/refsnp/{rsID[2:]}"
        r = requests.get(url)
        dnSNP_dict = r.json() if r else ''
    else:
        dnSNP_dict = ''

    return rsID, cellBase_dict, dnSNP_dict
