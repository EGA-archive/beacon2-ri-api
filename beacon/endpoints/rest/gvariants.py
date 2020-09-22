import logging

from ...utils import db
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


def build_response_individuals(rows, qparams_db, non_accessible_datasets):
    return build_beacon_response(rows,
                                 qparams_db,
                                 non_accessible_datasets,
                                 build_biosample_or_individual_response,
                                 variant_id=qparams_db.targetIdReq)

build_response_biosamples = build_response_individuals

def build_response_gvariants(rows, qparams_db, non_accessible_datasets):
    return build_beacon_response(rows,
                                 qparams_db,
                                 non_accessible_datasets,
                                 build_variant_response,
                                 variant_id=qparams_db.targetIdReq)


handler_individuals = generic_handler('individuals', individuals_proxy, db.fetch_individuals_by_variant, build_biosample_or_individual_response)
handler_biosamples  = generic_handler('biosamples' , biosamples_proxy , db.fetch_biosamples_by_variant , build_biosample_or_individual_response)
handler_gvariants   = generic_handler('gvariants'  , gvariants_proxy  , db.fetch_variants_by_variant   , build_variant_response)
