"""Access levels Endpoint.
The access levels endpoint reveals information about the access levels
of the different fields on the beacon can query.

.. note:: See ``beacon_api/utils`` folder ``access_levels.yml`` for changing values used here.
"""
import sys
import os
from pathlib import Path
import yaml
import logging

from .exceptions import BeaconAccesLevelsError, BeaconServerError
from .. import __id__, __beacon_name__, __apiVersion__

LOG = logging.getLogger(__name__)
"""Load the logging configurations from a YAML file."""

_here = Path(__file__).parent
ACCESS_LEVELS_FILE = os.getenv('BEACON_ACCESS_LEVELS', _here.parent / "utils/access_levels.yml")

# ----------------------------------------------------------------------------------------------------------------------
#                                         YAML LOADER
# ----------------------------------------------------------------------------------------------------------------------

def _find_yml_and_load(input_file):
    """Try to load the access levels yaml and return it as a dict."""
    _file = Path(input_file)

    if not _file.exists():
        LOG.error(f"The file '{_file}' does not exist", file=sys.stderr)
        return

    if _file.suffix in ('.yaml', '.yml'):
        with open(_file, 'r') as stream:
            file_dict = yaml.safe_load(stream)
            return file_dict

    # Otherwise, fail
    LOG.error(f"Unsupported format for {_file}", file=sys.stderr)


# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

async def special_datasets(db_pool):
  """ Fetch the special datasets (with different access levels).
  They are stored in the dataset_access_level_table in the DB.
  Return a dict prepared to be shown in the response.
  """
  async with db_pool.acquire(timeout=180) as connection:
    datasets = []
    try:
      query = "SELECT * FROM dataset_access_level_table;"
      LOG.debug(f"QUERY to fetch pecial datasets access levels info: {query}")
      statement = await connection.prepare(query)
      db_response =  await statement.fetch()

      datasets = {}
      for record in list(db_response):
        record_dict = dict(record)
        dataset_id = record_dict.get("dataset_id")
        parent_field = record_dict.get("parent_field")
        field = record_dict.get("field")
        access_level = record_dict.get("access_level")
        if dataset_id not in datasets.keys():
          datasets[dataset_id] = {}
          datasets[dataset_id][parent_field] = {}
        if not field:
          datasets[dataset_id][parent_field]["accessLevelSummary"] = access_level
        else:
          datasets[dataset_id][parent_field][field] = access_level

      return datasets
    except Exception as e:
            raise BeaconServerError(f'Query resulting special access levels datasets DB error: {e}') 



async def get_access_levels(request):
  """
  Parse the yaml file located in utils to retrieve the access levels information simplified of including field details.
  To change the access levels you should modify that file.
  Returns a dictionary prepared to represent it in the response.
  """
  # First we parse the request
  if request.method == 'POST':
    LOG.info('Parsed POST request body.')
    processed_request = await request.json()  # we are always expecting JSON
  else:
    processed_request = {k: v for k, v in request.rel_url.query.items()}

  for k, v in processed_request.items():
    if k != "includeFieldDetails":
      raise BeaconAccesLevelsError(f"Provided filed: '{k}' is not correct for the access levels endpoint", 'The only combination of field and input available is: includeFieldDetails=true')
    if  k == "includeFieldDetails" and v != "true":
      raise BeaconAccesLevelsError(f"Provided input: '{v}' is not correct for field: 'includeFieldDetails'", 'The only combination of field and input available is: includeFieldDetails=true')

  # Decide whether the response is simplified or complete and create it
  yml_dict = _find_yml_and_load(ACCESS_LEVELS_FILE)

  if processed_request.get("includeFieldDetails"):
    return yml_dict
  else:
    simplified_dict = {}
    for field, field_details_dict in yml_dict.items():
      try:
        simplified_dict[field] = field_details_dict["accessLevelSummary"]
      
      except Exception as e:
        raise BeaconAccesLevelsError(f"Couldn\'t get the {e} parameter from the '{field}' field", 'Please, make sure the access levels yaml file includes this information for every field')
    return simplified_dict


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER FUNCTION
# ----------------------------------------------------------------------------------------------------------------------

async def access_levels_terms_handler(db_pool, request):
    """Construct the `Beacon` app access level dict.
    """
    access_level_fields = await get_access_levels(request)

    beacon_answer = {        
        'id': '.'.join(reversed(request.host.split('.'))),
        # 'id': __id__,
        'name': __beacon_name__,
        'apiVersion': __apiVersion__,
        'fields': access_level_fields,
        'datasets': await special_datasets(db_pool)
    }

    return beacon_answer
