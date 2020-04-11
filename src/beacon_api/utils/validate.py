"""JSON Request/Response Validation and Token authentication (not implemented yet).
"""

import json
import re
import os
import logging
from functools import wraps


#from ..schemas import load_schema
from ..api.exceptions import (BeaconUnauthorised,
                              BeaconBadRequest,
                              BeaconForbidden,
                              BeaconServerError,
                              BeaconServicesBadRequest,
                              BeaconAccessLevelsBadRequest)

LOG = logging.getLogger(__name__)


# # SAMPLES
# def further_validation_sample(request, query_params):
#     """
#     It  takes a dictionary of the request parameters and checks the correct
#     combination of parameters, the lack of required parameters, etc. It takes
#     the validation a step further from the syntax validation that is done with
#     the JSON schema. 
#     """

#     def bad_request(m):
#         raise BeaconBadRequest(query_params, request.host, m)

#     start = query_params.get("start")
#     end = query_params.get("end")

#     if end and not start:
#         bad_request("'end' can't be provided without 'start'")

#     # Define values with the result of the get()
#     referenceName = query_params.get("referenceName")
#     assemblyId = query_params.get("assemblyId")

#     if start and (not referenceName or not assemblyId):
#         bad_request("'referenceName' and 'assemblyId' are requiered when 'start' is given")

#     referenceBases = query_params.get("referenceBases")
#     alternateBases = query_params.get("alternateBases")

#     if not start and (referenceBases or alternateBases):
#         bad_request("'start' is needed when using 'referenceBases' or 'alternateBases'")
     
#     ## to be continued...?

# def further_validation(endpoint, request, obj):
#     # Further validation
#     if endpoint == "query":
#         further_validation_query(request, obj)
#     elif endpoint == "genomic_region":
#         start = obj.get("start")
#         end = obj.get("end")
#         if end <= start:
#             raise BeaconBadRequest(obj, request.host, "'end' must be greater than 'start'")
#     elif endpoint == "sample_list":
#         further_validation_sample(request, obj)
      
