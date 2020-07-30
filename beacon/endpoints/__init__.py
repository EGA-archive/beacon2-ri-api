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
* ``/genomic_query`` -  querying/filtering datasets in the Beacon that contain a certain SNP or that contain variants inside a certain region;
* ``/genomic_snp`` -  querying/filtering datasets in the Beacon that contain a certain SNP;
* ``/genomic_region`` -  querying/filtering datasets in the Beacon that contain variants inside a certain region;
* ``/samples`` -  querying/filtering samples in the Beacon that match certain parameters and/or contain a certain variant;
* ``/individuals`` -  querying/filtering individuals in the Beacon that match certain parameters and/or contain a certain variant;
"""

from aiohttp import web

from . import (info,
                datasets,
                filtering_terms,
                access_levels,
                # query,
                # genomic_query,
                individuals,
                biosamples,
                gvariants,
                test, # only useful when testing
               )

routes = [
    # Info
    web.get('/'                 , info.handler),
    web.get('/info'             , info.handler),
    web.get('/service-info'     , info.handler_ga4gh_service_info),

    # Datasets
    web.get('/datasets'          , datasets.handler),

    # Filtering terms
    web.get('/filtering_terms'  , filtering_terms.handler),

    # Access levels
    web.get('/access_levels'    , access_levels.handler),

    # Schemas
    # web.get('/schemas'          , schemas.handler),

    # Query
    # web.get('/query'                            , query.handler),

    # Genomic query
    # web.get('/genomic_snp'                      , genomic_query.handler),
    # web.get('/genomic_region'                   , genomic_query.handler),

    # # Individuals
    web.get('/individuals'                              , individuals.handler_individuals),
    web.get('/individuals/{target_id_req}'              , individuals.handler_individuals),
    web.get('/individuals/{target_id_req}/g_variants'   , individuals.handler_gvariants),
    web.get('/individuals/{target_id_req}/biosamples'   , individuals.handler_biosamples),
    # web.post('/individuals', individuals.handler),
    # web.post('/individuals/{target_id_req}', individuals.handler),

    # # Biosamples
    web.get('/biosamples'                               , biosamples.handler_biosamples),
    web.get('/biosamples/{target_id_req}'               , biosamples.handler_biosamples),
    web.get('/biosamples/{target_id_req}/g_variants'    , biosamples.handler_gvariants),
    web.get('/biosamples/{target_id_req}/individuals'   , biosamples.handler_individuals),
    # web.post('/biosamples'                 , biosamples.handler),
    # web.post('/biosamples/{target_id_req}' , biosamples.handler),
    
    # # gvariant
    web.get('/g_variants'                               , gvariants.handler_gvariants),
    web.get('/g_variants/{target_id_req}'               , gvariants.handler_gvariants),
    web.get('/g_variants/{target_id_req}/biosamples'    , gvariants.handler_biosamples),
    web.get('/g_variants/{target_id_req}/individuals'   , gvariants.handler_individuals),


    # Just for test
    web.get('/test'                      , test.handler),

]

