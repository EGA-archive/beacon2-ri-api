#
# Supported Schemas
#
from . import default, alternative

supported_schemas = {
    # default
    'beacon-info-v2.0.0-draft.3': default.beacon_info_v30,
    'beacon-dataset-v2.0.0-draft.3': default.beacon_dataset_info_v30,
    'beacon-variant-v2.0.0-draft.3': default.beacon_variant_v30,
    'beacon-variant-annotation-v2.0.0-draft.3': default.beacon_variant_annotation_v30,
    'beacon-biosample-v2.0.0-draft.3': default.beacon_biosample_v30,
    'beacon-individual-v2.0.0-draft.3': default.beacon_individual_v30,
    'beacon-cohort-v2.0.0-draft.3.1': default.beacon_cohort_v31,
    # alternative
    'ga4gh-service-info-v1.0': alternative.ga4gh_service_info_v10,
    # phenopackets format
    'ga4gh-phenopacket-variant-v1.0': alternative.ga4gh_phenopackets_variant_v10,
    'ga4gh-phenopacket-variant-annotation-v1.0': alternative.ga4gh_phenopackets_variant_annotation_v10,
    'ga4gh-phenopacket-individual-v1.0': alternative.ga4gh_phenopackets_individual_v10,
    'ga4gh-phenopacket-biosample-v1.0': alternative.ga4gh_phenopackets_biosamples_v10,
    # variant representation format
    'ga4gh-variant-representation-v1.1': alternative.ga4gh_vr_variant_v11,
}
