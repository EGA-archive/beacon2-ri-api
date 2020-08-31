
from aiohttp import web

from . import rest, html

# only for testing
from . import test

routes = [
    # Info
    web.get('/api'                  , rest.info.handler),
    web.get('/api/info'             , rest.info.handler),
    web.get('/api/service-info'     , rest.info.handler_ga4gh_service_info),

    # Datasets
    web.get('/api/datasets'         , rest.datasets.handler),

    # Filtering terms
    web.get('/api/filtering_terms'   , rest.filtering_terms.handler),

    # Access levels
    # web.get('/api/access_levels'    , access_levels.handler),

    # Schemas
    # web.get('/api/schemas'          , schemas.handler),

    # Query
    # web.get('/api/query'                            , query.handler),

    # Genomic query
    # web.get('/api/genomic_snp'                      , genomic_query.handler),
    # web.get('/api/genomic_region'                   , genomic_query.handler),

    # Individuals
    web.get('/api/individuals'                              , rest.individuals.handler_individuals),
    web.get('/api/individuals/{target_id_req}'              , rest.individuals.handler_individuals),
    web.get('/api/individuals/{target_id_req}/g_variants'   , rest.individuals.handler_gvariants),
    web.get('/api/individuals/{target_id_req}/biosamples'   , rest.individuals.handler_biosamples),

    # Biosamples
    web.get('/api/biosamples'                               , rest.biosamples.handler_biosamples),
    web.get('/api/biosamples/{target_id_req}'               , rest.biosamples.handler_biosamples),
    web.get('/api/biosamples/{target_id_req}/g_variants'    , rest.biosamples.handler_gvariants),
    web.get('/api/biosamples/{target_id_req}/individuals'   , rest.biosamples.handler_individuals),
    
    # GVariant
    web.get('/api/g_variants'                               , rest.gvariants.handler_gvariants),
    web.get('/api/g_variants/{target_id_req}'               , rest.gvariants.handler_gvariants),
    web.get('/api/g_variants/{target_id_req}/biosamples'    , rest.gvariants.handler_biosamples),
    web.get('/api/g_variants/{target_id_req}/individuals'   , rest.gvariants.handler_individuals),


    ## HTML UI
    web.get('/', html.handlers.index, name='query'),
    web.get('/', html.handlers.index, name='snp'),
    web.get('/', html.handlers.index, name='region'),
    web.get('/', html.handlers.index, name='samples'),

    # # Auth endpoints
    web.get('/', html.handlers.index, name='privacy'),
    web.get('/login', html.auth.login, name='login'),
    web.get('/logout', html.auth.logout, name='logout'),

    # web.get('/snp', BeaconSNPView.as_view(), name='snp'),
    # web.get('/region', BeaconRegionView.as_view(), name='region'),
    # web.get('/samples', BeaconSamplesView.as_view(), name='samples'),
    # # Access Levels
    # web.get('/access-levels', BeaconAccessLevelsView.as_view(), name='levels'),
    # # Filtering terms
    # web.get('/terms', BeaconFilteringTermsView.as_view(), name='filters'),
    # web.get('/terms/', BeaconFilteringTermsView.as_view(), name='filters/'),
    # web.get('/terms/<term>', BeaconFilteringTermsView.as_view(), name='filters-term'),

    # AJAX
    web.get('/filtering_terms/{term}', html.filtering_terms.handler),

    # Just for test
    web.get('/api/test'                  , test.handler),
    web.get('/test'                      , test.handler),
]
