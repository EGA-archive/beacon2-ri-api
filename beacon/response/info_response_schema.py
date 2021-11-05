from beacon import conf
from beacon.request import RequestParams


# LOG = logging.getLogger(__name__)


def build_response_summary(exists, num_total_results):
    return {
        'exists': exists,
        'numTotalResults': num_total_results
    }


def build_beacon_handovers():
    return conf.beacon_handovers


def build_beacon_resultset_response(data,
                                    num_total_results,
                                    qparams: RequestParams,
                                    func_response_type):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams),
        'responseSummary': build_response_summary(bool(data), num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'beaconHandovers': build_beacon_handovers(),
        'response': {
            'resultSets': [ build_response(data, num_total_results, qparams, func_response_type) ]
        }
    }
    return beacon_response


def build_beacon_info_response(data, qparams, func_response_type, authorized_datasets=None):
    """"Fills the `results` part with the format for BeaconInfo"""

    if authorized_datasets is None:
        authorized_datasets = []

    meta = build_meta(qparams)

    response = func_response_type(data, qparams, authorized_datasets)

    beacon_response = {
        'meta': meta,
        'response': response,
    }

    return beacon_response


# def build_beacon_response(data, qparams_converted, func_response_type, authorized_datasets=[]):
#     """"
#     Transform data into the Beacon response format.
#     """

#     beacon_response = {
#         'meta': build_meta(qparams_converted),
#         'response': build_response(data, qparams_converted, func_response_type, authorized_datasets)
#     }
#     return beacon_response

def build_meta(qparams: RequestParams):
    """"Builds the `meta` part of the response

    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """

    meta = {
        'beaconId': conf.beacon_id,
        'apiVersion': conf.api_version,
        'returnedGranularity': conf.beacon_granularity,
        'receivedRequestSummary': {
            "apiVersion": qparams.meta.api_version,
            "requestedSchemas": qparams.meta.requested_schemas,
            "filters": qparams.query.filters,
            "includeResultsetResponses": qparams.query.include_resultset_responses,
            "pagination": {
                "skip": qparams.query.pagination.skip,
                "limit": qparams.query.pagination.limit
            },
            "requestedGranularity": qparams.meta.requested_granularity
        },
        'returnedSchemas': []
    }
    return meta


def build_response(data, num_total_results, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""

    # LOG.debug('Calling f= %s', func)
    results = func(data, qparams)

    response = {
        'id': '',
        'setType': '',
        'exists': bool(data),
        'resultsCount': len(results),
        'results': results,
        # 'info': None,
        'resultsHandover': None,  # build_results_handover
    }

    # if non_accessible_datasets:
    #     response['error'] = build_error(non_accessible_datasets)

    return response
