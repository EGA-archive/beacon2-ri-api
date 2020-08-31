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


from . import (filtering_terms,
               info,
               datasets,
               biosamples,
               gvariants,
               individuals)
