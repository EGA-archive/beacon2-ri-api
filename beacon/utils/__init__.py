import logging
from ..utils.json import jsonb


LOG = logging.getLogger(__name__)


def filter_hstore(hstores, schema_name):
    for hstore in hstores:
        v = hstore.get(schema_name, None)
        if v is not None and v != '{}':
            yield jsonb(v)
