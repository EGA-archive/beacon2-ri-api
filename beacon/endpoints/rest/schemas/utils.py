from ....utils.json import jsonb

def filter_hstore(hstores, schema_name):
    for hstore in hstores:
        v = hstore.get(schema_name, None)
        if v is not None:
            yield jsonb(v)
