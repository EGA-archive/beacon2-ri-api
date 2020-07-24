"""
Access levels Endpoint.
The access levels endpoint reveals information about the access levels
of the different fields on the beacon can query.

.. note:: See ``beacon_api/utils`` folder ``access_levels.yml`` for changing values used here.
"""
import sys
import os
import logging
from pathlib import Path
import yaml
from aiohttp.web import json_response


from .. import conf, load_access_levels
from ..utils.db import access_levels_datasets
from ..utils.exceptions import BeaconAccessLevelsBadRequest
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import BooleanField, ListField

LOG = logging.getLogger(__name__)

try:
    ACCESS_LEVELS_DICT = load_access_levels()
except Exception as e: # or just OSError?
    LOG.error("Error loading the access levels: %s", e)
    ACCESS_LEVELS_DICT = {}



def valid_fields_iter():
    for k, v in ACCESS_LEVELS_DICT.items():
        yield k
        if isinstance(v, dict):
            yield from v.keys()

VALID_FIELDS = set(valid_fields_iter())
VALID_LEVELS = ["public", "registered", "controlled", "not_supported"]

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class AccessLevelsParameters(RequestParameters):
    includeFieldDetails = BooleanField(default=False)
    displayDatasetDifferences = BooleanField(default=False)
    levels = ListField(default=[])
    datasetIds = ListField(default=None)
    fields = ListField(default=[])
    # fields = ChoiceField("public", "registered", "controlled", "not_supported", default="not_supported")

    def correlate(self, req, values):
        # values is a namedtuple, with the above keys

        for field in values.fields:
            if field not in VALID_FIELDS:
                raise BeaconAccessLevelsBadRequest(f"{field} is not a valid field")

        for level in values.levels:
            if level not in VALID_LEVELS:
                raise BeaconAccessLevelsBadRequest(f"{level} is not a valid level")

        # valid_datasets = [k for k in special_simple.keys()]
        # for dataset in values.datasetIds:
        #     if dataset not in valid_datasets:
        #         raise BeaconAccessLevelsBadRequest("Dataset not found")
  

# ----------------------------------------------------------------------------------------------------------------------
#                                         BASIC FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

def ignore_field_details_fields(dict_obj):
  """Takes a dict of the fields or the special datasets and removes everything that is not
  inside the accesslevelsSummary parent_field"""
  final_dict = {}

  for parent_field in dict_obj:
      final_dict[parent_field] = {}
      for field in dict_obj[parent_field]:
          if field == "accessLevelSummary":
              final_dict[parent_field] = dict_obj[parent_field][field]
              
  return final_dict

def ignore_field_details_special(dict_obj):
  """Takes a dict of the fields or the special datasets and removes everything that is not
  inside the accesslevelsSummary parent_field"""
  final_dict = {}

  for dataset in dict_obj: 
      final_dict[dataset] = {}
      for parent_field in dict_obj[dataset]:
          for field in dict_obj[dataset][parent_field]:
              if field == "accessLevelSummary":
                  final_dict[dataset][parent_field] = dict_obj[dataset][parent_field][field]

  return final_dict


def filter_by_field(fields, dic):
  """
  Recursive function that iterates through the response dict and filters
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
  Recursive function that iterates through the response dict and filters
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
#                                         MAIN FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def special_datasets():
    """ Fetch the special datasets (with different access levels).
    They are stored in the dataset_access_level_table in the DB.
    Return two dicts prepared to be shown in the response (one for displayDatasetDifferences=false, the other for true).
    """
  
    simple_datasets, datasets = {}, {}
    async for record in access_levels_datasets():
        dataset_id, access_level = record["dataset_id"], record["access_level"]
        parent_field, field = record["parent_field"], record["field"]

        if parent_field == "accessLevelSummary":
            simple_datasets[dataset_id] = access_level

        d = datasets.get(dataset_id)
        if d is None:
            if parent_field != "accessLevelSummary":
                datasets[dataset_id] = { parent_field: { field: access_level } }
        else:
            dd = d.get(parent_field)
            if dd is None:
                if parent_field != "accessLevelSummary":
                    d[parent_field] = { field: access_level }
            else:
                dd[field] = access_level

    #datasets = {k: v for k,v in datasets.items() if len(v) > 0} # removing dataset ids with no special access levels
    return simple_datasets, datasets



# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

proxy = AccessLevelsParameters()

async def handler(request):
    """Construct the `Beacon` app access level dict.
    """
    LOG.info('Running an access_levels request')
    
    # Load the yml file with the access_levels defined
    fields = ACCESS_LEVELS_DICT

    # Fetch the dict of the special access_levels datasets
    special_simple, special_all = await special_datasets()

    # Validate the query parameters
    qparams_raw, qparams_db = await proxy.fetch(request)

    # Print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy, LOG)

    ########### Daz: Commented out, cuz needs to be updated
    # # Further validation for datasets
    # selected_datasets = qparams_db.datasets[0]
    # for dataset in selected_datasets:
    #     if dataset not in special_simple:
    #         raise BeaconAccessLevelsBadRequest(f"{dataset} not found")

    # Handle first parameter: displayDatasetDifferences
    special = special_all if qparams_db.displayDatasetDifferences else special_simple
  
    ########### Daz: Commented out, cuz needs to be updated
    # # Handle second parameter = datasetIds
    # if qparams_db.datasetIds: 
    #     special = {k: v for k, v in special.items() if k in qparams_db.datasetIds}

    # Handle third parameter: includeFieldDetails
    if not qparams_db.includeFieldDetails and qparams_db.displayDatasetDifferences:
        fields = ignore_field_details_fields(ACCESS_LEVELS_DICT)
        special = ignore_field_details_special(special)
    elif not qparams_db.includeFieldDetails and not qparams_db.displayDatasetDifferences:
        fields = ignore_field_details_fields(ACCESS_LEVELS_DICT)

    # Handle forth parameter: fields
    if qparams_db.fields:
        fields = filter_by_field(qparams_db.fields, fields)
        special = filter_by_field(qparams_db.fields, special)

    # Handle fifth parameter: access_level
    if qparams_db.levels:
        fields = filter_by_access(qparams_db.levels, fields)
        special = filter_by_access(qparams_db.levels, special)

    beacon_answer = {        
        'id': conf.beacon_id,
        'name': conf.beacon_name,
        'apiVersion': conf.api_version,
        'fields': fields,
        'datasets': special
    }

    return json_response(beacon_answer)
