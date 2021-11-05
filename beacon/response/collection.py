
from beacon.request import RequestParams
from beacon.response.info_response_schema import build_beacon_handovers, build_meta, build_response, build_response_summary


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