"""
Beacon API endpoints.

The endpoints reflect the specification provided by:
- v1: https://github.com/ga4gh-beacon/specification/blob/develop/beacon.md
- v2: TBD

Endpoints:
* ``/api/``and ``/api/info`` -  Information about the datasets in the Beacon;
* ``/api/service-info`` and ``/api/info?model=GA4GH-ServiceInfo-v0.1`` -  Information about the Beacon (GA4GH Specification);
* ``/api/services`` -  Information about the services, required by the Beacon Network;
* ``/api/access_levels`` -  Information about the access levels of the Beacon;
* ``/api/filtering terms`` -  Information about existing ontology filters in the Beacon;
* ``/api/query`` -  querying/filtering datasets in the Beacon;
* ``/api/genomic_query`` -  querying/filtering datasets in the Beacon that contain a certain SNP or that contain variants inside a certain region;
* ``/api/genomic_snp`` -  querying/filtering datasets in the Beacon that contain a certain SNP;
* ``/api/genomic_region`` -  querying/filtering datasets in the Beacon that contain variants inside a certain region;
* ``/api/samples`` -  querying/filtering samples in the Beacon that match certain parameters and/or contain a certain variant;
* ``/api/individuals`` -  querying/filtering individuals in the Beacon that match certain parameters and/or contain a certain variant;

The others are HTML endpoints (ie the UI)
"""


# ====================================
# Common parameters
# ====================================

from ...utils.exceptions import BeaconBadRequest
from ...validation.fields import RegexField, IntegerField, SchemasField, Field, ChoiceField, ListField
from ...validation.request import RequestParameters

class GVariantParameters(RequestParameters):
    start = IntegerField(min_value=0, default=None) # TODO must accept 1 or 2 values
    end = IntegerField(min_value=0, default=None) # TODO must accept 1 or 2 values
    referenceBases = RegexField(r'^([ACGT]+)$', ignore_case=True, default=None)
    alternateBases = RegexField(r'^([ACGT]+)$', ignore_case=True, default=None)
    referenceName = ChoiceField("1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14",
                                "15", "16", "17", "18", "19", "20",
                                "21", "22", "X", "Y", "MT")
    # startMin = IntegerField(min_value=0)
    # startMax = IntegerField(min_value=0)
    # endMin = IntegerField(min_value=0)
    # endMax = IntegerField(min_value=0)
    includeDatasetResponses = ChoiceField("NONE", "ALL", "HIT", "MISS", default="NONE")
    assemblyId = RegexField(r'^((GRCh|hg)[0-9]+([.]?p[0-9]+)?)$', ignore_case=True, default=None)
    variantType = ChoiceField("DEL", "INS", "DUP", "INV", "CNV", "SNP", "MNP", "DUP:TANDEM", "DEL:ME", "INS:ME", "BND")
    filters = ListField(items=RegexField(r'.*:.+=?>?<?[0-9]*$'), default=None)
    datasetIds = ListField(default=[])
    # TODO implement fusions
    mateName = ChoiceField("1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14",
                                "15", "16", "17", "18", "19", "20",
                                "21", "22", "X", "Y", "MT")
    # requested schemas
    requestedSchemasVariant = SchemasField()
    requestedSchemasVariantAnnotation = SchemasField()
    requestedSchemasBiosample = SchemasField()
    requestedSchemasIndividual = SchemasField()
    apiVersion = RegexField(r'^v[0-9]+(\.[0-9]+)*$')
    # pagination
    skip = IntegerField(min_value=0, default=0)
    limit = IntegerField(min_value=1, default=10)
    targetIdReq = Field(default=None)

    def correlate(self, req, values):

        if values.targetIdReq is not None and (
                values.start is not None
                or values.end is not None
                or values.referenceBases is not None
                or values.alternateBases is not None
                or values.assemblyId is not None
                or values.referenceName is not None):
            raise BeaconBadRequest("No other parameters are accepted when querying by Id")


        if values.variantType and values.alternateBases != "N":
            raise BeaconBadRequest("If 'variantType' is provided then 'alternateBases' must be empty or equal to 'N'")

        if values.start is not None and values.end is not None and values.start > values.end:
            raise BeaconBadRequest("'start' must be less than 'end'")

        if values.referenceBases is not None and (values.alternateBases is None or values.start is None):
            raise BeaconBadRequest("If 'referenceBases' is provided then 'alternateBases' and ' start' are required")

        if (values.referenceBases is not None or values.alternateBases is not None) and values.end is not None:
            raise BeaconBadRequest("'referenceBases' cannot be combined with 'end'")

        if (values.start or values.referenceName or values.alternateBases or values.variantType or values.end ) \
                and (values.referenceName is None or values.assemblyId is None):
            raise BeaconBadRequest("'assemblyId' and 'referenceName' are mandatory")

        # TODO validation of start[0], start[1], end[0] and end[1]

        if values.mateName:
            raise BeaconBadRequest("Queries using 'mateName' are not implemented (yet)")
