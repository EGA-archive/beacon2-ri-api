
from aiohttp import web

from .rest import (filtering_terms,
                   info,
                   datasets,
                   biosamples,
                   gvariants,
                   individuals)



from . import html

# only for testing
from . import test

routes = [
    # Info
    web.get('/api'                  , info.handler),
    web.get('/api/info'             , info.handler),
    web.get('/api/service-info'     , info.handler_ga4gh_service_info),

    # Datasets
    web.get('/api/datasets'         , datasets.handler),

    # Filtering terms
    web.get('/api/filtering_terms'   , filtering_terms.handler),

    # Schemas
    # web.get('/api/schemas'          , schemas.handler),

    # Genomic query
    # web.get('/api/genomic_snp'                      , genomic_query.handler),
    # web.get('/api/genomic_region'                   , genomic_query.handler),

    # Individuals
    web.get('/api/individuals'                              , individuals.handler_individuals),
    web.get('/api/individuals/{target_id_req}'              , individuals.handler_individuals),
    web.get('/api/individuals/{target_id_req}/g_variants'   , individuals.handler_gvariants),
    web.get('/api/individuals/{target_id_req}/biosamples'   , individuals.handler_biosamples),

    # Biosamples
    web.get('/api/biosamples'                               , biosamples.handler_biosamples),
    web.get('/api/biosamples/{target_id_req}'               , biosamples.handler_biosamples),
    web.get('/api/biosamples/{target_id_req}/g_variants'    , biosamples.handler_gvariants),
    web.get('/api/biosamples/{target_id_req}/individuals'   , biosamples.handler_individuals),
    
    # GVariant
    web.get('/api/g_variants'                               , gvariants.handler_gvariants),
    web.get('/api/g_variants/{target_id_req}'               , gvariants.handler_gvariants),
    web.get('/api/g_variants/{target_id_req}/biosamples'    , gvariants.handler_biosamples),
    web.get('/api/g_variants/{target_id_req}/individuals'   , gvariants.handler_individuals),


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