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

from ..api.exceptions import BeaconUnauthorised, BeaconBadRequest, BeaconForbidden, BeaconServerError, BeaconServicesBadRequest, BeaconAccessLevelsBadRequest
from ..schemas import load_schema

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                                PARSING FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------


async def parse_request_object(request):
    """Parse as JSON Object depending on the request method.

    For POST request parse the body, while for the GET request parse the query parameters.
    """
    if request.method == 'POST':
        LOG.info('Parsed POST request body.')
        return request.method, await request.json()  # we are always expecting JSON

    if request.method == 'GET':
        # LOG.info(f"This is the request object: {request}")
        # LOG.info(f"These are the request.items: {request.rel_url.query.items()}")
        
        # GET parameters are returned as strings
        int_params = ['start', 'end', 'endMax', 'endMin', 'startMax', 'startMin']
        items = {k: (int(v) if k in int_params else v) for k, v in request.rel_url.query.items()}
        if 'datasetIds' in items:
            items['datasetIds'] = request.rel_url.query.get('datasetIds').split(',')
        elif 'filters' in items:
            items['filters'] = request.rel_url.query.get('filters').split(',')
        elif 'customFilters' in items:
            items['customFilters'] = request.rel_url.query.get('customFilters').split(',')
        obj = json.dumps(items)
        LOG.info('Parsed GET request parameters.')
        return request.method, json.loads(obj)


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


def extend_with_default(validator_class):
    """Include default values present in JSON Schema.

    Source: https://python-jsonschema.readthedocs.io/en/latest/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance
    """
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


DefaultValidatingDraft7Validator = extend_with_default(Draft7Validator)


# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY END POINT FURTHER VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

def further_validation_query(request, request_dict):
    """
    It  takes a dictionary of the request parameters and checks the correct
    combination of parameters, the lack of required parameters, etc. It takes
    the validation a step further from the syntax validation that is done with
    the JSON schema. 
    """

    # Define values with the result of the get()
    referenceName = request_dict.get("referenceName")
    assemblyId = request_dict.get("assemblyId")
    referenceBases = request_dict.get("referenceBases")
    alternateBases = request_dict.get("alternateBases")
    variantType = request_dict.get("variantType")
    start = request_dict.get("start")
    end = request_dict.get("end")
    startMin = request_dict.get("startMin")
    startMax = request_dict.get("startMax")
    endMin = request_dict.get("endMin")
    endMax =  request_dict.get("endMax")
    mateName = request_dict.get("mateName")

    # Do the checking
    if not referenceName or not assemblyId or not referenceBases:
        raise BeaconBadRequest(request_dict, request.host, "All 'referenceName', 'referenceBases' and/or 'assemblyId' are required")
    if not variantType and not alternateBases:
        raise BeaconBadRequest(request_dict, request.host, "Either 'alternateBases' or 'variantType' is required")
    elif variantType and (alternateBases and alternateBases != "N"):
        raise BeaconBadRequest(request_dict, request.host, "If 'variantType' is provided then 'alternateBases' must be empty or equal to 'N'")

    if not start:
        if end:
            raise BeaconBadRequest(request_dict, request.host, "'start' is required if 'end' is provided")
        elif not startMin and not startMax and not endMin and not endMax:
            raise BeaconBadRequest(request_dict, request.host, "Either 'start' or all of 'startMin', 'startMax', 'endMin' and 'endMax' are required")
        elif not startMin or not startMax or not endMin or not endMax:
            raise BeaconBadRequest(request_dict, request.host, "All of 'startMin', 'startMax', 'endMin' and 'endMax' are required")
    else:
        if startMin or startMax or endMin or startMax:
            raise BeaconBadRequest(request_dict, request.host, "'start' cannot be provided at the same time as 'startMin', 'startMax', 'endMin' and 'endMax'")
        if not end and referenceBases == "N":
            raise BeaconBadRequest(request_dict, request.host, "'referenceBases' cannot be 'N' if 'start' is provided and 'end' is missing")

    if variantType != 'BND' and end and end < start:
        raise BeaconBadRequest(request_dict, request.host, "'end' must be greater than 'start'")
    if endMin and endMin > endMax:
        raise BeaconBadRequest(request_dict, request.host, "'endMin' must be smaller than 'endMax'")
    if startMin and startMin > startMax:
        raise BeaconBadRequest(request_dict, request.host, "'startMin' must be smaller than 'startMax'") 

    if mateName:
        raise BeaconBadRequest(request_dict, request.host, "Queries using 'mateName' are not implemented")

# ----------------------------------------------------------------------------------------------------------------------
#                                   SAMPLE_LIST ENDPOINT FURTHER VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

def further_validation_sample(request, request_dict):
    """
    It  takes a dictionary of the request parameters and checks the correct
    combination of parameters, the lack of required parameters, etc. It takes
    the validation a step further from the syntax validation that is done with
    the JSON schema. 
    """

    # Define values with the result of the get()
    referenceName = request_dict.get("referenceName")
    assemblyId = request_dict.get("assemblyId")
    referenceBases = request_dict.get("referenceBases")
    alternateBases = request_dict.get("alternateBases")
    start = request_dict.get("start")
    end = request_dict.get("end")
    filters = request_dict.get("filters")
    datasetIds = request_dict.get("datasetIds")

    # Do the checking
    if end and not start:
        raise BeaconBadRequest(request_dict, request.host, "'end' can't be provided without 'start'")
    if start and (not referenceName or not assemblyId):
        raise BeaconBadRequest(request_dict, request.host, "'referenceName' and 'assemblyId' are requiered when 'start' is given")
    if not start and (referenceBases or alternateBases):
        raise BeaconBadRequest(request_dict, request.host, "'start' is needed when using 'referenceBases' or 'alternateBases'")
     
    ## to be continued...

      

# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN VALIDATION FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

def validate(endpoint):
    """
    Validate against JSON schema an return something.

    Return a parsed object if there is a POST.
    If there is a get do not return anything just validate.
    """
    def wrapper(func):

        @wraps(func) # just to get the documentation of the decorated function (beacon_get_query(request))
        async def wrapped(request, *args):
            if not isinstance(request, web.Request):
                raise BeaconBadRequest(request, request.host, "invalid request: This does not seem a valid HTTP Request.")
            try:
                _, obj = await parse_request_object(request)
            except Exception:
                raise BeaconServerError("Could not properly parse the provided Request Body as JSON.")
            try:
                # jsonschema.validate(obj, schema)
                LOG.info('Validate against JSON schema.')
                schema = load_schema(endpoint)
                DefaultValidatingDraft7Validator(schema).validate(obj)
            except ValidationError as e:
                if len(e.path) > 0:
                    LOG.error(f'Bad Request: {e.message} caused by input: {e.instance} in {e.path[0]}')
                    raise BeaconBadRequest(obj, request.host, f"Provided input: '{e.instance}' is not correct for field: '{e.path[0]}'")
                else:
                    LOG.error(f'Bad Request: {e.message} caused by input: {e.instance}')
                    raise BeaconBadRequest(obj, request.host, f"Provided input: '{e.instance}' is not correct because: '{e.message}'")
            
            # Further validation
            if endpoint == "query":
                further_validation_query(request, obj)
            elif  endpoint == "genomic_snp":
                LOG.debug("The genomic_snp endpoint does not require further validation")
            elif endpoint == "genomic_region":
                start = obj.get("start")
                end = obj.get("end")
                if end < start:
                    raise BeaconBadRequest(obj, request.host, "'end' must be greater than 'start'")
            elif endpoint == "sample_list":
                further_validation_sample(request, obj)

            return await func(request, *args)
        return wrapped
    return wrapper


def validate_services(func):
    """
    Same as before but adapted to the services endpoint. It calls a different parser function and error.
    """

    async def wrapped(request, *args):
        if not isinstance(request, web.Request):
            raise BeaconServicesBadRequest(request, request.host, "invalid request: This does not seem a valid HTTP Request.")
        try:
            _, obj = await parse_basic_request_object(request)
        except Exception:
            raise BeaconServerError("Could not properly parse the provided Request Body as JSON.")
        try:
            # jsonschema.validate(obj, schema)
            LOG.info('Validate against JSON schema.')
            schema = load_schema("services")
            DefaultValidatingDraft7Validator(schema).validate(obj)
        except ValidationError as e:
            if len(e.path) > 0:
                LOG.error(f'Bad Request: {e.message} caused by input: {e.instance} in {e.path[0]}')
                raise BeaconServicesBadRequest(obj, request.host, f"Provided input: '{e.instance}' is not correct for field: '{e.path[0]}', {e.message}")
            else:
                LOG.error(f'Bad Request: {e.message} caused by input: {e.instance}')
                raise BeaconServicesBadRequest(obj, request.host, f"Provided input: '{e.instance}' is not correct because: '{e.message}'")

        return await func(request, *args)
    return wrapped


def validate_access_levels(func):
    """
    Same as before but adapted to the access levels endpoint. It calls a different parser function and error.
    """

    async def wrapped(request, *args):
        if not isinstance(request, web.Request):
            raise BeaconServicesBadRequest(request, request.host, "invalid request: This does not seem a valid HTTP Request.")
        try:
            _, obj = await parse_basic_request_object(request)
        except Exception:
            raise BeaconServerError("Could not properly parse the provided Request Body as JSON.")
        try:
            # jsonschema.validate(obj, schema)
            LOG.info('Validate against JSON schema.')
            schema = load_schema("access_levels")
            DefaultValidatingDraft7Validator(schema).validate(obj)
        except ValidationError as e:
            if len(e.path) > 0:
                LOG.error(f'Bad Request: {e.message} caused by input: {e.instance} in {e.path[0]}')
                raise BeaconAccessLevelsBadRequest(request.host, f"Provided input: '{e.instance}' is not correct for field: '{e.path[0]}', {e.message}")
            else:
                LOG.error(f'Bad Request: {e.message} caused by input: {e.instance}')
                raise BeaconAccessLevelsBadRequest(request.host, f"Provided input: '{e.instance}' is not correct because: '{e.message}'")

        return await func(request, *args)
    return wrapped
