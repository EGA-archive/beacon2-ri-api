#
# Supported Schemas
#
from . import default, alternative

supported_schemas = {
    # default
    'beacon-info-v2.0.0-draft.2': default.beacon_info_v20,
    'beacon-dataset-v2.0.0-draft.2': default.beacon_dataset_info_v20,
    'beacon-variant-v2.0.0-draft.2': default.beacon_variant_v20,
    'beacon-variant-annotation-v2.0.0-draft.2': default.beacon_variant_annotation_v20,
    'beacon-biosample-v2.0.0-draft.2': default.beacon_biosample_v20,
    'beacon-individual-v2.0.0-draft.2': default.beacon_individual_v20,
    # alternative
    'ga4gh-service-info-v1.0': alternative.ga4gh_service_info_v10,
    # phenopackets format
    'ga4gh-phenopacket-variant-v1.0': alternative.ga4gh_phenopackets_variant_v10,
    'ga4gh-phenopacket-variant-annotation-v1.0': alternative.ga4gh_phenopackets_variant_annotation_v10,
    'ga4gh-phenopacket-individual-v1.0': alternative.ga4gh_phenopackets_individual_v10,
    'ga4gh-phenopacket-biosample-v1.0': alternative.ga4gh_phenopackets_biosamples_v10,
}
