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
    # phenopackets format
    'ga4gh-phenopacket-individual-v1.0': alternative.ga4gh_phenopackets_individual_v10,
    'ga4gh-phenopacket-biosample-v1.0': alternative.ga4gh_phenopackets_biosamples_v10,
    'ga4gh-phenopacket-variant-v1.0': alternative.ga4gh_phenopackets_variant_v10,
    'ga4gh-phenopacket-variant-annotation-v1.0': alternative.ga4gh_phenopackets_variant_annotation_v10,
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


def find_requested_schemas(default_type, requested_schema):
    """
    Returns the default schema for this type if none has been requested.
    Otherwise, returns the requested schemas.
    """
    if not requested_schema:
        return [DEFAULT_SCHEMAS[default_type]]

    valid_schemas = requested_schema[0]
    return [s for s,_ in valid_schemas]
