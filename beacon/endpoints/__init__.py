
from aiohttp import web

from . import (info,
               filtering_terms,
               access_levels,
               query,
               # genomic_query,
               # individuals,
               # biosamples,
               # gvariant,
               test, # only useful when testing
               )

routes = [
    # Info
    web.get('/api/'                 , info.handler_root),
    web.get('/api/info'             , info.handler_info),
    web.get('/api/service-info'     , info.handler_service_info),

    # Filtering terms
    web.get('/api/filtering_terms'  , filtering_terms.handler),

    # Access levels
    web.get('/api/access_levels'    , access_levels.handler),

    # Schemas
    # web.get('/api/schemas'          , schemas.handler),

    # Query
    web.get('/api/query'                            , query.handler),

    # Genomic query
    # web.get('/genomic_snp'                      , genomic_query.handler)
    # web.get('/genomic_region'                   , genomic_query.handler)

    # # Individuals
    # web.get('/api/individuals'                 , individuals.handler),
    # web.get('/api/individuals/{target_id_req}' , individuals.handler),
    # web.post('/api/individuals'                , individuals.handler),
    # web.post('/api/individuals/{target_id_req}', individuals.handler),

    # # Biosamples
    # web.get('/api/biosamples'                               , biosamples.handler),
    # web.get('/api/biosamples/{target_id_req}'               , biosamples.handler),
    # web.get('/api/biosamples/{target_id_req}/g_variants'    , biosamples.handler_gvariants),
    # # web.get('/api/biosamples/{target_id_req}/individuals' , biosamples.handler),
    # # web.post('/api/biosamples'                 , biosamples.handler),
    # # web.post('/api/biosamples/{target_id_req}' , biosamples.handler),
    
    # # gvariant
    # web.get('/api/gvariant'                      , gvariant.handler)
    # web.get('/api/g_variants/{target_id_req}'               , viral.handler_gvariants),
    # web.get('/api/g_variants/{target_id_req}/biosamples'    , viral.handler_biosamples),
    # web.get('/api/g_variants/{target_id_req}/individuals' , viral.handler_individuals),


    # Just for test
    web.get('/test'                      , test.handler),

]

