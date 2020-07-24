"""
Validation module à la Django
"""

from ..utils.exceptions import BeaconBadRequest
from .fields import RegexField, IntegerField, SchemasField, Field
from .request import RequestParameters

class ValidationError(Exception):
    pass


class GVariantParameters(RequestParameters):
    start = IntegerField(min_value=0, default=None)
    end = IntegerField(min_value=0, default=None)
    referenceBases = RegexField(r'^([ACGT]+)$', ignore_case=True, default=None)
    alternateBases = RegexField(r'^([ACGT]+)$', ignore_case=True, default=None)
    requestedSchemasVariant = SchemasField()
    requestedSchemasVariantAnnotation = SchemasField()
    requestedSchemasBiosample = SchemasField()
    requestedSchemasIndividual = SchemasField()
    apiVersion = RegexField(r'^v[0-9]+(\.[0-9]+)*$')
    targetIdReq = Field(default=None)

    def correlate(self, req, values):

        if values.targetIdReq is not None and (values.start is not None or values.end
         is not None or values.referenceBases is not None or values.alternateBases is not None):
            raise BeaconBadRequest("No other parameters are accepted when querying by Id")

        if values.start is not None and values.end is not None and values.start > values.end:
            raise BeaconBadRequest("'start' must be less than 'end'")

        if values.referenceBases is not None and (values.alternateBases is None or values.start is None):
            raise BeaconBadRequest("If 'referenceBases' is provided then 'alternateBases' and ' start' are required")

        if (values.referenceBases is not None or values.alternateBases is not None) and values.end is not None:
            raise BeaconBadRequest("'referenceBases' cannot be combined with 'end'")
