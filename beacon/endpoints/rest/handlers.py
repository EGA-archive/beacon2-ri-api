from ...utils import db
from .response.response_schema import (build_variant_response,
                                       build_biosample_or_individual_response)
from . import BiosamplesParameters, GVariantsParameters, IndividualsParameters, generic_handler

biosamples_proxy = BiosamplesParameters()
gvariants_proxy = GVariantsParameters()
individuals_proxy = IndividualsParameters()

individuals_by_biosample = generic_handler('individuals', individuals_proxy, db.fetch_individuals_by_biosample, build_biosample_or_individual_response)
biosamples_by_biosample = generic_handler('biosamples' , biosamples_proxy , db.fetch_biosamples_by_biosample , build_biosample_or_individual_response)
gvariants_by_biosample = generic_handler('gvariants'  , gvariants_proxy  , db.fetch_variants_by_biosample   , build_variant_response)

individuals_by_variant = generic_handler('individuals', individuals_proxy, db.fetch_individuals_by_variant, build_biosample_or_individual_response)
biosamples_by_variant = generic_handler('biosamples' , biosamples_proxy , db.fetch_biosamples_by_variant , build_biosample_or_individual_response)
gvariants_by_variant = generic_handler('gvariants'  , gvariants_proxy  , db.fetch_variants_by_variant   , build_variant_response)

individuals_by_individual = generic_handler('individuals', individuals_proxy, db.fetch_individuals_by_individual, build_biosample_or_individual_response)
biosamples_by_individual = generic_handler('biosamples' , biosamples_proxy , db.fetch_biosamples_by_individual , build_biosample_or_individual_response)
gvariants_by_individual = generic_handler('gvariants'  , gvariants_proxy  , db.fetch_variants_by_individual   , build_variant_response)
