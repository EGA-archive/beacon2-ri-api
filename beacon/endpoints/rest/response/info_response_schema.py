import logging

from .... import conf

LOG = logging.getLogger(__name__)


def build_beacon_response(data, qparams_converted, func_response_type, authorized_datasets=[]):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams_converted, func_response_type),
        'response': build_response(data, qparams_converted, func_response_type, authorized_datasets)
    }
    return beacon_response


def build_meta(qparams, func_response_type):
    """"Builds the `meta` part of the response

    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """

    meta = {
        'beaconId': conf.beacon_id,
        'apiVersion': conf.api_version,
        'receivedRequest': build_received_request(qparams),
        'returnedSchemas': [qparams.requestedSchema[0]]
    }
    return meta


def build_received_request(qparams):
    """"Fills the `receivedRequest` part with the request data"""

    request = {
        'meta': {
            'requestedSchemas' : [qparams.requestedSchema[0]],
            'apiVersion' : qparams.apiVersion,
        },
    }

    return request


def build_error(qparams):
    """"
    Fills the `error` part in the response.
    This error only applies to partial errors which do not prevent the Beacon from answering.
    """

    message = 'Some error.'

    return {
        'error': {
            'errorCode': 206,
            'errorMessage': message
        }
    }


def build_response(data, qparams, func, authorized_datasets=[]):
    """"Fills the `response` part with the correct format in `results`"""

    response = {
            'results': func(data, qparams, authorized_datasets),
            'info': None,
            # 'resultsHandover': None, # build_results_handover
            # 'beaconHandover': None, # build_beacon_handover
        }

    # build_error(qparams)

    return response


def build_service_info_response(datasets, qparams, authorized_datasets=[]):
    """"Fills the `results` part with the format for ServiceInfo"""

    func = qparams.requestedSchema[1]

    return func(datasets, authorized_datasets)


def build_dataset_info_response(data, qparams, authorized_datasets=[]):
    """"Fills the `results` part with the format for Dataset"""

    func = qparams.requestedSchema[1]
    return [func(row, authorized_datasets) for row in data]


def build_formatted_response(data, func):
    """"Fills the `results` part with the format defined in func"""
    return [func(row) for row in data]