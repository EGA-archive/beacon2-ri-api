import logging

from ...utils import resolve_token, db
from ...utils.exceptions import BeaconUnauthorised
from ...utils.stream import json_stream
from .response.response_schema import (build_beacon_response,
                                       build_variant_response,
                                       build_biosample_or_individual_response)
from . import BiosamplesParameters, GVariantsParameters, IndividualsParameters, generic_handler

LOG = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

biosamples_proxy = BiosamplesParameters()
gvariants_proxy = GVariantsParameters()
individuals_proxy = IndividualsParameters()


def fetch_individuals(qparams_db, datasets, authenticated):
    return db.fetch_individuals(qparams_db, datasets, authenticated, individual_stable_id=qparams_db.targetIdReq)

def fetch_biosamples(qparams_db, datasets, authenticated):
    return db.fetch_biosamples(qparams_db, datasets, authenticated, individual_stable_id=qparams_db.targetIdReq)

def fetch_variants(qparams_db, datasets, authenticated):
    return db.fetch_variants(qparams_db, datasets, authenticated, individual_stable_id=qparams_db.targetIdReq)


def build_response_individuals(rows, qparams_db, non_accessible_datasets):
    return build_beacon_response(rows,
                                 qparams_db,
                                 non_accessible_datasets,
                                 build_biosample_or_individual_response,
                                 individual_id=qparams_db.targetIdReq)

build_response_biosamples = build_response_individuals

def build_response_gvariants(rows, qparams_db, non_accessible_datasets):
    return build_beacon_response(rows,
                                 qparams_db,
                                 non_accessible_datasets,
                                 build_variant_response,
                                 individual_id=qparams_db.targetIdReq)



handler_individuals = generic_handler('individuals', individuals_proxy, fetch_individuals, build_biosample_or_individual_response)
handler_biosamples  = generic_handler('biosamples' , biosamples_proxy , fetch_biosamples , build_biosample_or_individual_response)
handler_gvariants   = generic_handler('gvariants'  , gvariants_proxy  , fetch_variants   , build_variant_response)
