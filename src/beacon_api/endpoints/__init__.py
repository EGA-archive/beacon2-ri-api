# package

from aiohttp import web

from . import (info,
               filtering_terms,
               access_levels,
            #    schemas,
               query,
            #    genomic_query,
               individuals,
            #    biosamples,
            #   gvariant,

               viral,

               # testing
               test
               )

routes = [
    # Info
    web.get('/'                 , info.handler_root),
    web.get('/info'             , info.handler_info),
    web.get('/service-info'     , info.handler_service_info),

    # Filtering terms
    web.get('/filtering_terms'  , filtering_terms.handler),

    # Access levels
    web.get('/access_levels'    , access_levels.handler),

    # Schemas
    # web.get('/schemas'          , schemas.handler),

    # Query
    web.get('/query'                            , query.handler),

    # Genomic query
    # web.get('/genomic_snp'                      , genomic_query.handler)
    # web.get('/genomic_region'                   , genomic_query.handler)

    # Individuals
    web.get('/individuals'                 , individuals.handler),
    web.get('/individuals/{target_id_req}' , individuals.handler),
    web.post('/individuals'                , individuals.handler),
    web.post('/individuals/{target_id_req}', individuals.handler),

    # Biosamples
    # web.get('/biosamples'                  , biosamples.handler),
    # web.get('/biosamples/{target_id_req}'  , biosamples.handler),
    # web.post('/biosamples'                 , biosamples.handler),
    # web.post('/biosamples/{target_id_req}' , biosamples.handler),
    
    # gvariant
    # web.get('/gvariant'                      , gvariant.handler)

    web.get('/test'                      , test.handler),

    web.get('/viral'                      , viral.handler),
    web.get('/viral_html'                 , viral.handler_html),

]

