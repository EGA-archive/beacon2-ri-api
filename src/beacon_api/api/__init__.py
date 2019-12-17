"""
Beacon API endpoints.

The endpoints reflect the specification provided by:
- v1: https://github.com/ga4gh-beacon/specification/blob/develop/beacon.md
- v2: TBD

Endpoints:
* ``/``and ``/info`` -  Information about the datasets in the Beacon;
* ``/service-info`` and ``/info?model=GA4GH-ServiceInfo-v0.1`` -  Information about the Beacon (GA4GH Specification);
* ``/services`` -  Information about the services, required by the Beacon Network;
* ``/access_levels`` -  Information about the access levels of the Beacon;
* ``/filtering terms`` -  Information about existing ontology filters in the Beacon;
* ``/query`` -  querying/filtering datasets in the Beacon;
* ``/genomic_snp`` -  querying/filtering datasets in the Beacon that contain a certain SNP;
* ``/genomic_region`` -  querying/filtering datasets in the Beacon that contain variants inside a certain region;
* ``/samples`` -  querying/filtering samples in the Beacon that match certain parameters and/or contain a certain variant;
* ``/individuals`` -  querying/filtering individuals in the Beacon that match certain parameters and/or contain a certain variant;
"""
