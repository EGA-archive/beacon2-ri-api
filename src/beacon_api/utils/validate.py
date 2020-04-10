"""JSON Request/Response Validation and Token authentication (not implemented yet).
"""

import json
import re
import os
import logging
from functools import wraps

import aiohttp
from aiohttp import web
from jsonschema import Draft7Validator, validators
from jsonschema.exceptions import ValidationError

#from ..schemas import load_schema
from ..api.exceptions import (BeaconUnauthorised,
                              BeaconBadRequest,
                              BeaconForbidden,
                              BeaconServerError,
                              BeaconServicesBadRequest,
                              BeaconAccessLevelsBadRequest,
                              capture_server_error)

LOG = logging.getLogger(__name__)

def load_schema(name):
    raise NotImplementedError('load_schema is unused')

# ----------------------------------------------------------------------------------------------------------------------
#                                                PARSING FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

def flatten_dict(input_dict):
    """
    Iterates through the post dictionary and
    it flattens it to mimic the get request. 

    We expect keys of the dictionary (and all sub-dict) to be unique
    """
    final_dict = {}
    for key, val in input_dict.items():
        if isinstance(val,dict):
            tmp_dict = flatten_dict(val)
            final_dict.update(tmp_dict)
        else:
            if val and val not in ["", "null", None]:
                final_dict[key] = ",".join(val)
    return final_dict


_INT_PARAMS = set(['start', 'end', 'endMax', 'endMin', 'startMax', 'startMin'])
_ARRAY_PARAMS = set(['datasetIds', 'filters', 'customFilters', 'individualSchemas'])

@capture_server_error(prefix="Could not properly parse the provided Request Body as JSON.")
async def parse_request_object(request):
    """
    Parse as JSON Object depending on the request method.

    For POST request parse the body, while for the GET request parse the parameters
    related to queries (if any).
    """
    if request.method == 'POST':
        post_request = await request.json()
        raw_request = flatten_dict(post_request) 
        LOG.info('Flattening POST request.')
    if request.method == 'GET':
        raw_request = dict(request.rel_url.query.items())

    # Some parameters are returned as strings, others as integers, and others as arrays
    for k, v in raw_request.items():
        if k in _INT_PARAMS:
            raw_request[k] = int(v)
        if k in _ARRAY_PARAMS:
            raw_request[k] = v.split(',')  # empty string -> []
        # others are kept as strings

    LOG.info('Parsed request parameters.')
    return request.method, raw_request


@capture_server_error(prefix="Could not properly parse the provided Request Body as JSON.")
async def parse_basic_request_object(request):
    """Parse as JSON Object depending on the request method.

    For POST request parse the body, while for the GET request parse the query parameters.
    """
    if request.method == 'POST':
        LOG.info('Parsed POST request body.')
        return request.method, await request.json()  # we are always expecting JSON

    if request.method == 'GET':        
        # GET parameters are returned as strings
        items = {k: v for k, v in request.rel_url.query.items() if k != "levels"}
        items.update({k: v.lower() for k, v in request.rel_url.query.items() if k == "levels"})
        obj = json.dumps(items)
        LOG.info('Parsed GET request parameters.')
        return request.method, json.loads(obj)

# ----------------------------------------------------------------------------------------------------------------------
#                                         VALIDATOR
# ----------------------------------------------------------------------------------------------------------------------

def extend_with_default(validator_class):
    """Include default values present in JSON Schema.

    Source: https://python-jsonschema.readthedocs.io/en/latest/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance
    """
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for prop, subschema in properties.items():
            default = subschema.get("default")
            if default is not None:
                instance.setdefault(prop, default)

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


DefaultValidatingDraft7Validator = extend_with_default(Draft7Validator)


# ----------------------------------------------------------------------------------------------------------------------
#                                         FURTHER VALIDATIONS
# ----------------------------------------------------------------------------------------------------------------------


# QUERY
def further_validation_query(request, query_params):
    """
    It  takes a dictionary of the request parameters and checks the correct
    combination of parameters, the lack of required parameters, etc. It takes
    the validation a step further from the syntax validation that is done with
    the JSON schema. 
    """

    def bad_request(m):
        raise BeaconBadRequest(query_params, request.host, m)

    # Define values with the result of the get()
    referenceName = query_params.get("referenceName")
    assemblyId = query_params.get("assemblyId")
    referenceBases = query_params.get("referenceBases")

    if not referenceName or not assemblyId or not referenceBases:
        bad_request("All 'referenceName', 'referenceBases' and/or 'assemblyId' are required")

    alternateBases = query_params.get("alternateBases")
    variantType = query_params.get("variantType")

    if not variantType and not alternateBases:
        bad_request("Either 'alternateBases' or 'variantType' is required")

    if variantType and alternateBases != "N":
        bad_request("If 'variantType' is provided then 'alternateBases' must be empty or equal to 'N'")

    start = query_params.get("start")
    end = query_params.get("end")
    startMin = query_params.get("startMin")
    startMax = query_params.get("startMax")
    endMin = query_params.get("endMin")
    endMax =  query_params.get("endMax")

    if not start:
        if end:
            bad_request("'start' is required if 'end' is provided")
        elif not startMin and not startMax and not endMin and not endMax:
            bad_request("Either 'start' or all of 'startMin', 'startMax', 'endMin' and 'endMax' are required")
        elif not startMin or not startMax or not endMin or not endMax:
            bad_request("All of 'startMin', 'startMax', 'endMin' and 'endMax' are required")
    else:
        if startMin or startMax or endMin or startMax:
            bad_request("'start' cannot be provided at the same time as 'startMin', 'startMax', 'endMin' and 'endMax'")
        if not end and referenceBases == "N":
            bad_request("'referenceBases' cannot be 'N' if 'start' is provided and 'end' is missing")

    if variantType != 'BND' and end and end < start:
        bad_request("'end' must be greater than 'start'")
    if endMin and endMin > endMax:
        bad_request("'endMin' must be smaller than 'endMax'")
    if startMin and startMin > startMax:
        bad_request("'startMin' must be smaller than 'startMax'") 

    mateName = query_params.get("mateName")
    if mateName:
        bad_request("Queries using 'mateName' are not implemented")


# SAMPLES
def further_validation_sample(request, query_params):
    """
    It  takes a dictionary of the request parameters and checks the correct
    combination of parameters, the lack of required parameters, etc. It takes
    the validation a step further from the syntax validation that is done with
    the JSON schema. 
    """

    def bad_request(m):
        raise BeaconBadRequest(query_params, request.host, m)

    start = query_params.get("start")
    end = query_params.get("end")

    if end and not start:
        bad_request("'end' can't be provided without 'start'")

    # Define values with the result of the get()
    referenceName = query_params.get("referenceName")
    assemblyId = query_params.get("assemblyId")

    if start and (not referenceName or not assemblyId):
        bad_request("'referenceName' and 'assemblyId' are requiered when 'start' is given")

    referenceBases = query_params.get("referenceBases")
    alternateBases = query_params.get("alternateBases")

    if not start and (referenceBases or alternateBases):
        bad_request("'start' is needed when using 'referenceBases' or 'alternateBases'")
     
    ## to be continued...?

      

# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN VALIDATION FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------
def convert_error(error_from, error_to):
    def wrapper(func):
        def decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_form as e:
                LOG.error('Bad Request: %s caused by input: %s%s',
                          e.message, e.instance, ' in '+str(e.path[0]) if e.path else '')
                raise error_to(obj,
                            request.host,
                            f"Provided input: '{e.instance}' is not correct for field: '{e.path[0]}'") from e
        return decorator
    return wrapper

def further_validation(endpoint, request, obj):
    # Further validation
    if endpoint == "query":
        further_validation_query(request, obj)
    elif endpoint == "genomic_region":
        start = obj.get("start")
        end = obj.get("end")
        if end <= start:
            raise BeaconBadRequest(obj, request.host, "'end' must be greater than 'start'")
    elif endpoint == "sample_list":
        further_validation_sample(request, obj)

# _SCHEMA = None

def _validate(endpoint, parse_func):
    """
    Validate against JSON schema.
    """
    def wrapper(func):

        @wraps(func) # just to get the documentation of the decorated function (beacon_get_query(request))
        async def decorator(request, *args):
            # assert isinstance(request, web.Request), "invalid request: This does not seem a valid HTTP Request."
            method, obj = await parse_func(request)

            # jsonschema.validate(obj, schema)
            LOG.info('Validate against JSON schema: %s', endpoint)
            # global _SCHEMA
            # if _SCHEMA is None:
            _SCHEMA = load_schema(endpoint)
            DefaultValidatingDraft7Validator(_SCHEMA).validate(obj)

            further_validation(endpoint, request, obj)

            return await func(method, obj, request, *args)
        return decorator
    return wrapper

@convert_error(ValidationError, BeaconBadRequest)
def validate(endpoint):
    return _validate(endpoint, parse_request_object)

@convert_error(ValidationError, BeaconServicesBadRequest)
def validate_services(func):
    return _validate("services", parse_basic_request_object)(func)

@convert_error(ValidationError, BeaconAccessLevelsBadRequest)
def validate_access_levels(func):
    return _validate("access_levels", parse_basic_request_object)(func)


validate_simple = validate
