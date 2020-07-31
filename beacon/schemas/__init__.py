from . import default, alternative

SUPPORTED_SCHEMAS = {
    # default
    'beacon-info-v2.0.0-draft.2': default.beacon_info_v20,
    'beacon-dataset-v2.0.0-draft.2': default.beacon_dataset_info_v20,
    'beacon-variant-v2.0.0-draft.2': default.beacon_variant_v20,
    'beacon-variant-annotation-v2.0.0-draft.2': default.beacon_variant_annotation_v20,
    'beacon-biosample-v2.0.0-draft.2': default.beacon_biosample_v20,
    'beacon-individual-v2.0.0-draft.2': default.beacon_individual_v20,
    # alternative
    'ga4gh-service-info-v1.0': alternative.ga4gh_service_info_v10,
    # TODO add phenopackets format
}


DEFAULT_SCHEMAS = {
    'ServiceInfo': 'beacon-info-v2.0.0-draft.2',
    'Dataset': 'beacon-dataset-v2.0.0-draft.2',
    'Variant': 'beacon-variant-v2.0.0-draft.2',
    'VariantAnnotation': 'beacon-variant-annotation-v2.0.0-draft.2',
    'Biosample': 'beacon-biosample-v2.0.0-draft.2',
    'Individual': 'beacon-individual-v2.0.0-draft.2',
}


def partition(schemas):
    valid, invalid = set(), set() # avoid repetitions
    for schema in schemas:
        func = SUPPORTED_SCHEMAS.get(schema)
        if func is None:
            invalid.add(schema)
        else:
            valid.add((schema,func))
    return (valid, invalid)
