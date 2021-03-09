from ...utils import db
from .response.response_schema import (build_variant_response,
                                       build_biosample_or_individual_response, 
                                       build_cohort_response,
                                       BeaconEntity)
from . import BiosamplesParameters, GVariantsParameters, IndividualsParameters, CohortParameters, generic_handler

biosamples_proxy = BiosamplesParameters()
gvariants_proxy = GVariantsParameters()
individuals_proxy = IndividualsParameters()
cohorts_proxy = CohortParameters()

individuals_by_biosample = generic_handler('individuals', BeaconEntity.BIOSAMPLE, individuals_proxy, db.fetch_individuals_by_biosample, db.count_individuals_by_biosample, build_biosample_or_individual_response)
biosamples_by_biosample = generic_handler('biosamples' , BeaconEntity.BIOSAMPLE, biosamples_proxy , db.fetch_biosamples_by_biosample , db.count_biosamples_by_biosample, build_biosample_or_individual_response)
gvariants_by_biosample = generic_handler('gvariants'  , BeaconEntity.BIOSAMPLE, gvariants_proxy  , db.fetch_variants_by_biosample   , db.count_variants_by_biosample, build_variant_response)

individuals_by_variant = generic_handler('individuals', BeaconEntity.VARIANT, individuals_proxy, db.fetch_individuals_by_variant, db.count_individuals_by_variant, build_biosample_or_individual_response)
biosamples_by_variant = generic_handler('biosamples' , BeaconEntity.VARIANT, biosamples_proxy , db.fetch_biosamples_by_variant , db.count_biosamples_by_variant, build_biosample_or_individual_response)
gvariants_by_variant = generic_handler('gvariants'  , BeaconEntity.VARIANT, gvariants_proxy  , db.fetch_variants_by_variant   , db.count_variants_by_variant, build_variant_response)

individuals_by_individual = generic_handler('individuals', BeaconEntity.INDIVIDUAL, individuals_proxy, db.fetch_individuals_by_individual, db.count_individuals_by_individual, build_biosample_or_individual_response)
biosamples_by_individual = generic_handler('biosamples' , BeaconEntity.INDIVIDUAL, biosamples_proxy , db.fetch_biosamples_by_individual , db.count_biosamples_by_individual, build_biosample_or_individual_response)
gvariants_by_individual = generic_handler('gvariants'  , BeaconEntity.INDIVIDUAL, gvariants_proxy  , db.fetch_variants_by_individual   , db.count_variants_by_individual, build_variant_response)

cohorts_by_cohort = generic_handler('cohorts'  , BeaconEntity.COHORT, cohorts_proxy  , db.fetch_cohorts_by_cohort   , db.count_cohorts_by_cohort, build_cohort_response)
