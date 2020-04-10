"""
Custom API exception reponses.

API specification requires custom messages upon error.
"""

import json
import logging
from functools import wraps

from aiohttp import web

from .. import conf

LOG = logging.getLogger(__name__)

# Only one of `alternateBases` or `variantType` is required, validated by schema
_fields = ['referenceName', 'referenceBases', 'assemblyId',
           'alternateBases', 'variantType', 'start', 'end', 'startMin', 'startMax',
           'endMin', 'endMax', 'ids']

def process_exception_data(request, host, error_code, error):
    """Return request data as dictionary."""
    LOG.error('Raising from %s: %s', host, error)
    
    alleleRequest = { k: request.get(k) for k in _fields }
    alleleRequest['includeDatasetResponses'] = request.get("includeDatasetResponses", "NONE")
        
    return {
        'beaconId': conf.beacon_id,
        "apiVersion": conf.api_version,
        'exists': None,
        'error': {'errorCode': error_code,
                  'errorMessage': error},
        'alleleRequest': alleleRequest,
        # showing empty datasetsAlleRsponse as no datasets found
        # A null/None would represent no data while empty array represents
        # none found or error and corresponds with exists null/None
        'datasetAlleleResponses': [],
    }


class BeaconBadRequest(web.HTTPBadRequest):
    """Exception returns with 400 code and a custom error message.

    The method is called if one of the required parameters are missing or invalid.
    Used in conjuction with JSON Schema validator.
    """

    def __init__(self, request, host, error):
        """Return custom bad request exception."""
        data = process_exception_data(request, host, 400, error)
        super().__init__(text=json.dumps(data),
                         content_type="application/json")


class BeaconUnauthorised(web.HTTPUnauthorized):
    """HTTP Exception returns with 401 code with a custom error message.

    The method is called if the user is not registered or if the token from the authentication has expired.
    Used in conjuction with Token authentication aiohttp middleware.
    """

    def __init__(self, request, host, error, error_message):
        """Return custom unauthorized exception."""
        data = process_exception_data(request, host, 401, error)
        headers_401 = {"WWW-Authenticate": f"Bearer realm=\"{conf.url}\"\n\
                         error=\"{error}\"\n\
                         error_description=\"{error_message}\""}
        super().__init__(text=json.dumps(data),
                         content_type="application/json",
                         # we use auth scheme Bearer by default
                         headers=headers_401)


class BeaconForbidden(web.HTTPForbidden):
    """HTTP Exception returns with 403 code with the error message.

    `'Resource not granted for authenticated user or resource protected for all users.'`.
    The method is called if the dataset is protected or if the user is authenticated
    but not granted the resource. Used in conjuction with Token authentication aiohttp middleware.
    """

    def __init__(self, request, host, error):
        """Return custom forbidden exception."""
        data = process_exception_data(request, host, 403, error)
        super().__init__(text=json.dumps(data),
                         content_type="application/json")


class BeaconServerError(web.HTTPInternalServerError):
    """HTTP Exception returns with 500 code with the error message.

    The 500 error is not specified by the Beacon API, thus as simple error would do.
    """

    def __init__(self, error):
        """Return custom forbidden exception."""
        data = {'errorCode': 500,
                'errorMessage': error}
        raise super().__init__(text=json.dumps(data),
                               content_type="application/json")


class BeaconAccesLevelsError(web.HTTPBadRequest):
    """BeaconAccesLevelsError Exception specific class.

    Generates custom exception messages based on request parameters.
    """

    def __init__(self, error, help_message):
        """Return custom forbidden exception."""
        LOG.error('400 ERROR MESSAGE: %s', error)
        data = {'errorCode': 400,
                'errorMessage': error,
                'help': help_message }
        super().__init__(text=json.dumps(data),
                         content_type="application/json")



class BeaconServicesBadRequest(web.HTTPBadRequest):
    """BeaconServicesBadRequest Exception specific class.

    Generates custom exception messages based on request parameters.
    """

    def __init__(self, query_parameters, host, error):
        """Return request data as dictionary."""
        LOG.error('400 ERROR MESSAGE: %s', error)
        data = {'beaconId': conf.beacon_id,
                'error': {'errorCode': 400,
                          'errorMessage': error },
                'servicesRequest': {'serviceType': query_parameters.get("serviceType", None),
                                    'model': query_parameters.get("model", None),
                                    'listFormat': query_parameters.get("listFormat", None),
                                    'apiVersion': query_parameters.get("apiVersion", None) }
        }
        super().__init__(text=json.dumps(data),
                         content_type="application/json")



class BeaconAccessLevelsBadRequest(web.HTTPBadRequest):
    """BeaconAccessLevelsBadRequest Exception specific class.

    Generates custom exception messages based on request parameters.
    """

    def __init__(self, host, error):
        """Return request data as dictionary."""
        LOG.error('400 ERROR MESSAGE: %s', error)
        data = {'beaconId': conf.beacon_id,
                'error': {'errorCode': 400,
                          'message': error},
                'fields': {}}
        super().__init__(text=json.dumps(data),
                         content_type="application/json")



class BeaconBasicBadRequest(web.HTTPBadRequest):
    """BeaconBASICBadRequest Exception specific class.

    Generates custom exception messages based on request parameters.
    """
    def __init__(self, request, host, error):
        """Return request data as dictionary."""
        LOG.error('400 ERROR MESSAGE: %s', error)
        data = { 'beaconId': conf.beacon_id,
                 'error': {'errorCode': 400,
                           'errorMessage': error},
                 'request': request if isinstance(request, dict) else dict(request) }
        super().__init__(text=json.dumps(data),
                         content_type="application/json")



def capture_server_error(prefix=''):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise BeaconServerError(f'{prefix}{e}') from e
        return decorator
    return wrapper
