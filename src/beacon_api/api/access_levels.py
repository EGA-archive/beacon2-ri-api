"""Access levels Endpoint.
The access levels endpoint reveals information about the access levels
of the different fields on the beacon can query.

.. note:: See ``beacon_api/utils`` folder ``access_levels.yml`` for changing values used here.
"""
import sys
import os
import logging
from pathlib import Path


from .exceptions import BeaconAccesLevelsError, BeaconServerError, BeaconAccessLevelsBadRequest
from .. import __id__, __beacon_name__, __apiVersion__
from ..utils.polyvalent_functions import find_yml_and_load

LOG = logging.getLogger(__name__)
"""Load the logging configurations from a YAML file."""

# Load the access levels dict
_here = Path(__file__).parent
ACCESS_LEVELS_FILE = os.getenv('BEACON_ACCESS_LEVELS', _here.parent / "utils/access_levels.yml")
ACCESS_LEVELS_DICT = find_yml_and_load(ACCESS_LEVELS_FILE)

# ----------------------------------------------------------------------------------------------------------------------
#                                         BASIC FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

def ignore_field_details(dict_obj, dict_type):
  """Takes a dict of the fields or the special datasets and removes everything that is not
  inside the accesslevelsSummary parent_field"""
  final_dict = {}

  if dict_type == "special":
    for dataset in dict_obj: 
      final_dict[dataset] = {}
      for parent_field in dict_obj[dataset]:
        for field in dict_obj[dataset][parent_field]:
          if field == "accessLevelSummary":
            final_dict[dataset][parent_field] = dict_obj[dataset][parent_field][field]

  elif dict_type == "fields":
    for parent_field in dict_obj:
      final_dict[parent_field] = {}
      for field in dict_obj[parent_field]:
        if field == "accessLevelSummary":
          final_dict[parent_field] = dict_obj[parent_field][field]

  return final_dict


def get_valid_levels(dic):
  """
  Recursive function to iterate trough each answer (fields and datasets) and gather
  the levels.
  Returns a list of the present levels.
  """
  levels_list = set()

  for key, value in dic.items():
    if type(value) == dict:
      levels_list = levels_list.union(get_valid_levels(value))
    else:
      levels_list.add(value)
  return levels_list


def custom_validation(request, processed_request, fields, special_simple, special_all):
  """
  Validate the access levels parameters that need special errors based on the existing values
  that you get after the query. 
  """
  fields_list = [] if not processed_request.get("fields") else processed_request.get("fields").split(",")
  levels_list = [] if not processed_request.get("levels") else processed_request.get("levels").split(",")
  datasetIds = None if not processed_request.get("datasetIds") else processed_request.get("datasetIds").split(",")

  valid_levels = ["public", "registered", "controlled", "not_supported"]
  valid_fields = list(set([k for k in fields.keys()] + [key for v in fields.values() for key in v]))
  # valid_levels = list(get_valid_levels(fields).union(get_valid_levels(special_simple).union(get_valid_levels(special_all)))) # valid_levels based on the ones that appear in the answer
  valid_datasets = [k for k in special_simple.keys()]
 
  if fields_list:
    for field in fields_list:
      if field not in valid_fields:
        BeaconAccessLevelsBadRequest(request.host, "Field not found")
  elif levels_list:
    for level in levels_list:
      if level not in valid_levels:
        BeaconAccessLevelsBadRequest(request.host, "Level not valid")
  elif datasetIds:
    for dataset in datasetIds:
      if dataset not in valid_datasets:
        BeaconAccessLevelsBadRequest(request.host, "Dataset not found")
  
  return fields_list, levels_list, datasetIds


def filter_by_field(fields, dic):
  """
  Recursive funciton that iterates through the response dict and filters
  the fields that are specified in a list.
  """
  output = {}
  
  for key, val in dic.items():
      if type(val) == dict and key not in fields:
          new_dict = filter_by_field(fields, val)
          if new_dict:
              output[key] = new_dict
      else:
          if key in fields:
              output[key] = val
  return output


def filter_by_access(levels, dic):
  """
  Recursive funciton that iterates through the response dict and filters
  the access_levels that are specified in a list.
  """
  output = {}
  
  for key, val in dic.items():
      if type(val) == dict:
          new_dict = filter_by_access(levels, val)
          if new_dict:
              output[key] = new_dict
      else:
          if val.lower() in levels:
              output[key] = val
  return output


# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

async def special_datasets(db_pool):
  """ Fetch the special datasets (with different access levels).
  They are stored in the dataset_access_level_table in the DB.
  Return two dicts prepared to be shown in the response (one for displayDatasetDifferences=false, the other for true).
  """
  async with db_pool.acquire(timeout=180) as connection:
    datasets = []
    try:
      query = """SELECT dt.stable_id, al.parent_field, al.field, al.access_level FROM dataset_access_level_table al
               JOIN beacon_dataset dt ON al.dataset_id=dt.id;"""
      LOG.debug(f"QUERY to fetch special datasets access levels info: {query}")
      statement = await connection.prepare(query)
      db_response =  await statement.fetch()
    except Exception as e:
      raise BeaconServerError(f'Query special access levels datasets DB error: {e}') 
    
    datasets = {}
    simple_datasets = {}
    for record in list(db_response):
      record_dict = dict(record)
      dataset_id = record_dict.get("stable_id")
      parent_field = record_dict.get("parent_field")
      field = record_dict.get("field")
      access_level = record_dict.get("access_level")
      if dataset_id not in datasets.keys():
        datasets[dataset_id] = {}
        datasets[dataset_id][parent_field] = {}
        datasets[dataset_id][parent_field][field] = access_level
        if parent_field == "accessLevelSummary":
          simple_datasets[dataset_id] = access_level
          datasets[dataset_id].pop("accessLevelSummary")
      else:
        if parent_field not in datasets[dataset_id].keys():
          datasets[dataset_id][parent_field] = {}
          datasets[dataset_id][parent_field][field] = access_level
        else:
          datasets[dataset_id][parent_field][field] = access_level

        if parent_field == "accessLevelSummary":
          simple_datasets[dataset_id] = access_level
          datasets[dataset_id].pop("accessLevelSummary")

    datasets = {k: v for k,v in datasets.items() if len(v) > 0} # removing dataset ids with no special access levels
    return simple_datasets, datasets


async def get_access_levels(request, processed_request, db_pool):
  """
  Parse the yaml file located in utils to retrieve the access levels information simplified of including field details.
  To change the access levels you should modify that file.
  Returns a dictionary prepared to represent it in the response.
  """
  # Load the yml file with the access_levels defined
  fields = ACCESS_LEVELS_DICT
  # Fetch the dict of the special access_levels datasets
  special_simple, special_all = await special_datasets(db_pool)

  # Validate the parameters passed
  fields_list, levels_list, datasetIds = custom_validation(request, processed_request, fields, special_simple, special_all)

  # Handle first parameter: displayDatasetDifferences
  displayDatasetDifferences = False if not processed_request.get("displayDatasetDifferences") or processed_request.get("displayDatasetDifferences").lower() == "false" else True
  if displayDatasetDifferences:
    special = special_all
  elif not displayDatasetDifferences:
    special = special_simple
  
  # Handle second parameter = datasetIds
  if datasetIds:
    special = {k: v for k, v in special.items() if k in datasetIds}

  # Handle third parameter: includeFieldDetails
  includeFieldDetails = False if not processed_request.get("includeFieldDetails") or processed_request.get("includeFieldDetails").lower() == "false" else True
  if not includeFieldDetails and displayDatasetDifferences:
    fields = ignore_field_details(fields, "fields")
    special = ignore_field_details(special, "special")
  elif not includeFieldDetails and not displayDatasetDifferences:
    fields = ignore_field_details(fields, "fields")

  # Handle forth parameter: fields
  if fields_list:
    fields = filter_by_field(fields_list, fields)
    special = filter_by_field(fields_list, special)

  # Handle fifth parameter: access_level
  if levels_list:
    fields = filter_by_access(levels_list, fields)
    special = filter_by_access(levels_list, special)

  return fields, special


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def access_levels_terms_handler(db_pool, processed_request, request):
    """Construct the `Beacon` app access level dict.
    """
    access_level_fields, special_datasets = await get_access_levels(request, processed_request, db_pool)

    beacon_answer = {        
        'id': '.'.join(reversed(request.host.split('.'))),
        'name': __beacon_name__,
        'apiVersion': __apiVersion__,
        'fields': access_level_fields,
        'datasets': special_datasets
    }

    return beacon_answer
