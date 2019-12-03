"""Custom API exception reponses.

API specification requires custom messages upon error.
"""

import json
import logging
from aiohttp import web

from .. import __apiVersion__
from ..conf import CONFIG_INFO

LOG = logging.getLogger(__name__)

class BeaconError(Exception):
    """BeaconError Exception specific class.

    Generates custom exception messages based on request parameters.
    """

    def __init__(self, request, host, error_code, error):
        """Return request data as dictionary."""
        self.data = {'beaconId': '.'.join(reversed(host.split('.'))),
                     "apiVersion": __apiVersion__,
                     'exists': None,
                     'error': {'errorCode': error_code,
                               'errorMessage': error},
                     'alleleRequest': {'referenceName': request.get("referenceName", None),
                                       'referenceBases': request.get("referenceBases", None),
                                       'includeDatasetResponses': request.get("includeDatasetResponses", "NONE"),
                                       'assemblyId': request.get("assemblyId", None)},
                     # showing empty datasetsAlleRsponse as no datasets found
                     # A null/None would represent no data while empty array represents
                     # none found or error and corresponds with exists null/None
                     'datasetAlleleResponses': []}
        # include ids only if they are specified
        # as per specification if they don't exist all datatsets will be queried
        # Only one of `alternateBases` or `variantType` is required, validated by schema
        oneof_fields = ["alternateBases", "variantType", "start", "end", "startMin", "startMax",
                        "endMin", "endMax", "ids"]
        self.data['alleleRequest'].update({k: request.get(k) for k in oneof_fields if k in request})
        return self.data


class BeaconBadRequest(BeaconError):
    """Exception returns with 400 code and a custom error message.

    The method is called if one of the required parameters are missing or invalid.
    Used in conjuction with JSON Schema validator.
    """

    def __init__(self, request, host, error):
        """Return custom bad request exception."""
        data = super().__init__(request, host, 400, error)

        LOG.error(f'400 ERROR MESSAGE: {error}')
        raise web.HTTPBadRequest(content_type="application/json", text=json.dumps(data))


class BeaconUnauthorised(BeaconError):
    """HTTP Exception returns with 401 code with a custom error message.

    The method is called if the user is not registered or if the token from the authentication has expired.
    Used in conjuction with Token authentication aiohttp middleware.
    """

    def __init__(self, request, host, error, error_message):
        """Return custom unauthorized exception."""
        data = super().__init__(request, host, 401, error)
        headers_401 = {"WWW-Authenticate": f"Bearer realm=\"{CONFIG_INFO.url}\"\n\
                         error=\"{error}\"\n\
                         error_description=\"{error_message}\""}
        LOG.error(f'401 ERROR MESSAGE: {error}')
        raise web.HTTPUnauthorized(content_type="application/json", text=json.dumps(data),
                                   # we use auth scheme Bearer by default
                                   headers=headers_401)


class BeaconForbidden(BeaconError):
    """HTTP Exception returns with 403 code with the error message.

    `'Resource not granted for authenticated user or resource protected for all users.'`.
    The method is called if the dataset is protected or if the user is authenticated
    but not granted the resource. Used in conjuction with Token authentication aiohttp middleware.
    """

    def __init__(self, request, host, error):
        """Return custom forbidden exception."""
        data = super().__init__(request, host, 403, error)

        LOG.error(f'403 ERROR MESSAGE: {error}')
        raise web.HTTPForbidden(content_type="application/json", text=json.dumps(data))


class BeaconServerError(BeaconError):
    """HTTP Exception returns with 500 code with the error message.

    The 500 error is not specified by the Beacon API, thus as simple error would do.
    """

    def __init__(self, error):
        """Return custom forbidden exception."""
        data = {'errorCode': 500,
                'errorMessage': error}

        LOG.error(f'500 ERROR MESSAGE: {error}')
        raise web.HTTPInternalServerError(content_type="application/json", text=json.dumps(data))


class BeaconAccesLevelsError(Exception):
    """BeaconAccesLevelsError Exception specific class.

    Generates custom exception messages based on request parameters.
    """

    def __init__(self, error, help):
        """Return custom forbidden exception."""
        data = {'errorCode': 400,
                'errorMessage': error,
                'help': help}

        LOG.error(f'400 ERROR MESSAGE: {error}')
        raise web.HTTPBadRequest(content_type="application/json", text=json.dumps(data))



class BeaconServicesBadRequest(Exception):
    """BeaconServicesBadRequest Exception specific class.

    Generates custom exception messages based on request parameters.
    """

    def __init__(self, processed_request, host, error):
        """Return request data as dictionary."""
        self.data = {'beaconId': '.'.join(reversed(host.split('.'))),
                     'error': {'errorCode': 400,
                               'errorMessage': error},
                     'servicesRequest': {'serviceType': processed_request.get("serviceType", None),
                                       'model': processed_request.get("model", None),
                                       'listFormat': processed_request.get("listFormat", None),
                                       'apiVersion': processed_request.get("apiVersion", None)}}
        LOG.error(f'400 ERROR MESSAGE: {error}')
        raise web.HTTPBadRequest(content_type="application/json", text=json.dumps(self.data))



class BeaconAccessLevelsBadRequest(Exception):
    """BeaconAccessLevelsBadRequest Exception specific class.

    Generates custom exception messages based on request parameters.
    """

    def __init__(self, host, error):
        """Return request data as dictionary."""
        self.data = {'beaconId': '.'.join(reversed(host.split('.'))),
                     'error': {'errorCode': 400,
                               'message': error},
                     'fields': {}}
        LOG.error(f'400 ERROR MESSAGE: {error}')
        raise web.HTTPBadRequest(content_type="application/json", text=json.dumps(self.data))



class BeaconBasicBadRequest(Exception):
    """BeaconBASICBadRequest Exception specific class.

    Generates custom exception messages based on request parameters.
    """
    def __init__(self, processed_request, host, error):
        """Return request data as dictionary."""
        self.data = {'beaconId': '.'.join(reversed(host.split('.'))),
                     'error': {'errorCode': 400,
                               'errorMessage': error},
                     'request': processed_request}
        LOG.error(f'400 ERROR MESSAGE: {error}')
        raise web.HTTPBadRequest(content_type="application/json", text=json.dumps(self.data))



