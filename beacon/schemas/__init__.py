from . import default, alternative

SUPPORTED_SCHEMAS = {
    'beacon-variant-v0.1': default.beacon_variant_v01,
    'beacon-variant-annotation-v0.1': default.beacon_variant_annotation_v01,
    'beacon-biosample-v0.1': default.beacon_biosample_v01,
    'beacon-individual-v0.1': default.beacon_individual_v01,
}


DEFAULT_SCHEMAS = {
    'Variant': 'beacon-variant-v0.1',
    'VariantAnnotation': 'beacon-variant-annotation-v0.1',
    'Biosample': 'beacon-biosample-v0.1',
    'Individual': 'beacon-individual-v0.1',
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
