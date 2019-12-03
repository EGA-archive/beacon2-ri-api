"""Load JSON Schemas.

The JSON schemas represent a good method of checking that an endpoint's
requests/responses adhere to the API specification.
Schemas available:

* ``query.json`` - for the ``/query`` endpoint request;
* ``genomic_snp.json`` - for the ``/genomic_snp`` endpoint response;
* ``genomic_region.json`` - for the ``/genomic_region`` endpoint request;
"""

import os
import json


def load_schema(name):
    """Load JSON schemas."""
    module_path = os.path.dirname(__file__)
    path = os.path.join(module_path, '{0}.json'.format(name))

    with open(os.path.abspath(path), 'r') as fp:
        data = fp.read()

    return json.loads(data)
