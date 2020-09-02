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


def make_response(error_code, error, fields=None):
    """Return request data as dictionary."""
    LOG.error('Error %s: %s', error_code, error)
    
    return {
        'meta': {
            'beaconId': conf.beacon_id,
            'apiVersion': conf.api_version,
            'receivedRequest': {
                'meta': {
                    'requestedSchemas': dict(fields or []),
                },
                'query': None,
            },
            'returnedSchemas': None,
        },
        'response': {
            'exists': None,
            'error': {'errorCode': error_code,
                      'errorMessage': error},
        },
    }

class BeaconBadRequest(web.HTTPBadRequest):
    """Exception returns with 400 code and a custom error message.

    The method is called if one of the required parameters are missing or invalid.
    Used in conjuction with JSON Schema validator.
    """
    _beacon_response = None
    def __init__(self, error, fields=None):
        """Return custom bad request exception."""
        self._beacon_response = make_response(400, error, fields=fields)
        super().__init__(reason=error)

class BeaconUnauthorised(web.HTTPUnauthorized):
    """HTTP Exception returns with 401 code with a custom error message.

    The method is called if the user is not registered or if the token from the authentication has expired.
    Used in conjuction with Token authentication aiohttp middleware.
    """
    _beacon_response = None
    def __init__(self, error, fields=None):
        """Return custom unauthorized exception."""
        self._beacon_response = make_response(401, error, fields=fields)
        super().__init__(reason=error,
                         # we use auth scheme Bearer by default
                         headers={"WWW-Authenticate": f'Bearer realm="{conf.url}"\nerror="{error}"'})


class BeaconForbidden(web.HTTPForbidden):
    """HTTP Exception returns with 403 code with the error message.

    `'Resource not granted for authenticated user or resource protected for all users.'`.
    The method is called if the dataset is protected or if the user is authenticated
    but not granted the resource. Used in conjuction with Token authentication aiohttp middleware.
    """
    _beacon_response = None
    def __init__(self, error, fields=None):
        """Return custom forbidden exception."""
        self._beacon_response = make_error(403, error, fields=fields)
        super().__init__(reason=error)


class BeaconServerError(web.HTTPInternalServerError):
    """HTTP Exception returns with 500 code with the error message.

    The 500 error is not specified by the Beacon API, thus as simple error would do.
    """
    _beacon_response = None
    def __init__(self, error):
        """Return custom forbidden exception."""
        self._beacon_response = {'errorCode': 500,
                                 'errorMessage': error}
        super().__init__(reason=error)


class BeaconServicesBadRequest(web.HTTPBadRequest):
    """BeaconServicesBadRequest Exception specific class.

    Generates custom exception messages based on request parameters.
    """
    _beacon_response = None
    def __init__(self, query_parameters, error):
        """Return request data as dictionary."""
        LOG.error('Error 400: %s', error)
        query_parameters = query_parameters or {}
        self._beacon_response = {'beaconId': conf.beacon_id,
                                 'error': {'errorCode': 400,
                                           'errorMessage': error },
                                 'servicesRequest': {'serviceType': query_parameters.get("serviceType", None),
                                                     'model': query_parameters.get("model", None),
                                                     'listFormat': query_parameters.get("listFormat", None),
                                                     'apiVersion': query_parameters.get("apiVersion", None) }
        }
        super().__init__(reason=error)
