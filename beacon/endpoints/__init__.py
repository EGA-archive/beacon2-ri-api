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

from ..ui.handlers import index
from ..ui.auth import login, logout

routes = [
    # Info
    web.get('/api'                 , info.handler),
    web.get('/api/info'             , info.handler),
    web.get('/api/service-info'     , info.handler_ga4gh_service_info),

    # Datasets
    web.get('/datasets'          , datasets.handler),

    # Filtering terms
    web.get('/api/filtering_terms'  , filtering_terms.handler),

    # Access levels
    web.get('/api/access_levels'    , access_levels.handler),

    # Schemas
    # web.get('/api/schemas'          , schemas.handler),

    # Query
    # web.get('/api/query'                            , query.handler),

    # Genomic query
    # web.get('/api/genomic_snp'                      , genomic_query.handler),
    # web.get('/api/genomic_region'                   , genomic_query.handler),

    # # Individuals
    web.get('/api/individuals'                              , individuals.handler_individuals),
    web.get('/api/individuals/{target_id_req}'              , individuals.handler_individuals),
    web.get('/api/individuals/{target_id_req}/g_variants'   , individuals.handler_gvariants),
    web.get('/api/individuals/{target_id_req}/biosamples'   , individuals.handler_biosamples),
    # web.post('/api/individuals', individuals.handler),
    # web.post('/api/individuals/{target_id_req}', individuals.handler),

    # # Biosamples
    web.get('/api/biosamples'                               , biosamples.handler_biosamples),
    web.get('/api/biosamples/{target_id_req}'               , biosamples.handler_biosamples),
    web.get('/api/biosamples/{target_id_req}/g_variants'    , biosamples.handler_gvariants),
    web.get('/api/biosamples/{target_id_req}/individuals'   , biosamples.handler_individuals),
    # web.post('/api/biosamples'                 , biosamples.handler),
    # web.post('/api/biosamples/{target_id_req}' , biosamples.handler),
    
    # # gvariant
    web.get('/api/g_variants'                               , gvariants.handler_gvariants),
    web.get('/api/g_variants/{target_id_req}'               , gvariants.handler_gvariants),
    web.get('/api/g_variants/{target_id_req}/biosamples'    , gvariants.handler_biosamples),
    web.get('/api/g_variants/{target_id_req}/individuals'   , gvariants.handler_individuals),


    # Just for test
    web.get('/api/test'                  , test.handler),
    web.get('/test'                      , test.handler),


    ## HTML UI
    web.get('/', index, name='query'),
    web.get('/', index, name='snp'),
    web.get('/', index, name='region'),
    web.get('/', index, name='samples'),

    # web.get('/snp', BeaconSNPView.as_view(), name='snp'),
    # web.get('/region', BeaconRegionView.as_view(), name='region'),
    # web.get('/samples', BeaconSamplesView.as_view(), name='samples'),
    # # Access Levels
    # web.get('/access-levels', BeaconAccessLevelsView.as_view(), name='levels'),
    # # Filtering terms
    # web.get('/terms', BeaconFilteringTermsView.as_view(), name='filters'),
    # web.get('/terms/', BeaconFilteringTermsView.as_view(), name='filters/'),
    # web.get('/terms/<term>', BeaconFilteringTermsView.as_view(), name='filters-term'),

    # # Auth endpoints
    web.get('/', index, name='privacy'),
    web.get('/login', login, name='login'),
    web.get('/logout', logout, name='logout'),

]

# from .views import (BeaconQueryView,
#                     BeaconSNPView,
#                     BeaconRegionView,
#                     BeaconAccessLevelsView,
#                     BeaconFilteringTermsView,
#                     TestingView,
#                     BeaconSamplesView)
# from .auth import BeaconLoginView, BeaconLogoutView

