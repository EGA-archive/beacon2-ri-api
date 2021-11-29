from beacon import conf
from beacon.request import RequestParams


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
            "requestParameters": qparams.query.request_parameters,
            "includeResultsetResponses": qparams.query.include_resultset_responses,
            "pagination": qparams.query.pagination,
            "requestedGranularity": qparams.meta.requested_granularity,
            "testMode": qparams.query.test_mode
        },
        'returnedSchemas': []
    }
    return meta


def build_beacon_handovers():
    return conf.beacon_handovers


def build_response_summary(exists, num_total_results):
    return {
        'exists': exists,
        'numTotalResults': num_total_results
    }


def build_response(data, num_total_results, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""

    # LOG.debug('Calling f= %s', func)
    results = func(data, qparams)

    response = {
        'id': '',
        'setType': '',
        'exists': bool(data),
        'resultsCount': num_total_results,
        'results': results,
        # 'info': None,
        'resultsHandover': None,  # build_results_handover
    }

    # if non_accessible_datasets:
    #     response['error'] = build_error(non_accessible_datasets)

    return response


########################################
# Resultset Response
########################################

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
        'response': {
            'resultSets': [build_response(data, num_total_results, qparams, func_response_type)]
        },
        'beaconHandovers': build_beacon_handovers(),
    }
    return beacon_response

########################################
# Collection Response
########################################

def build_beacon_collection_response(data, num_total_results, qparams: RequestParams, func_response_type):
    beacon_response = {
        'meta': build_meta(qparams),
        'responseSummary': build_response_summary(bool(data), num_total_results),
        # TODO: 'info': build_extended_info(),
        'beaconHandovers': build_beacon_handovers(),
        'response': {
            'collections': [ build_response(data, num_total_results, qparams, func_response_type) ]
        }
    }
    return beacon_response

########################################
# Info Response
########################################

def build_beacon_info_response(data, qparams, func_response_type, authorized_datasets=None):
    if authorized_datasets is None:
        authorized_datasets = []

    beacon_response = {
        'meta': build_meta(qparams),
        'response': {
            'id': conf.beacon_id,
            'name': conf.beacon_name,
            'apiVersion': conf.api_version,
            'environment': conf.environment,
            'organization': {
                'id': conf.org_id,
                'name': conf.org_name,
                'description': conf.org_description,
                'address': conf.org_adress,
                'welcomeUrl': conf.org_welcome_url,
                'contactUrl': conf.org_contact_url,
                'logoUrl': conf.org_logo_url,
            },
            'description': conf.description,
            'version': conf.version,
            'welcomeUrl': conf.welcome_url,
            'alternativeUrl': conf.alternative_url,
            'createDateTime': conf.create_datetime,
            'updateDateTime': conf.update_datetime,
            'datasets': func_response_type(data, qparams, authorized_datasets),
        }
    }

    return beacon_response

########################################
# Service Info Response
########################################

def build_beacon_service_info_response():
    beacon_response = {
        'id': conf.beacon_id,
        'name': conf.beacon_name,
        'type': {
            'group': conf.ga4gh_service_type_group,
            'artifact': conf.ga4gh_service_type_artifact,
            'version': conf.ga4gh_service_type_version
        },
        'description': conf.description,
        'organization': {
            'name': conf.org_name,
            'url': conf.org_welcome_url
        },
        'contactUrl': conf.org_contact_url,
        'documentationUrl': conf.documentation_url,
        'createdAt': conf.create_datetime,
        'updatedAt': conf.update_datetime,
        'environment': conf.environment,
        'version': conf.version,
    }

    return beacon_response

########################################
# Error Response
########################################

def build_error(non_accessible_datasets):
    """"
    Fills the `error` part in the response.
    This error only applies to partial errors which do not prevent the Beacon from answering.
    """

    message = f'You are not authorized to access some of the requested datasets: {non_accessible_datasets}'

    return {
        'error': {
            'errorCode': 401,
            'errorMessage': message
        }
    }
