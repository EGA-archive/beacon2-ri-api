from . import default, alternative

SUPPORTED_SCHEMAS = {
    'beacon-variant-v2.0': default.beacon_variant_v20,
    'beacon-variant-annotation-v2.0': default.beacon_variant_annotation_v20,
    'beacon-biosample-v2.0': default.beacon_biosample_v20,
    'beacon-individual-v2.0': default.beacon_individual_v20,
}


DEFAULT_SCHEMAS = {
    'Variant': 'beacon-variant-v2.0',
    'VariantAnnotation': 'beacon-variant-annotation-v2.0',
    'Biosample': 'beacon-biosample-v2.0',
    'Individual': 'beacon-individual-v2.0',
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
