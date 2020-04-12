# package

from aiohttp import web

from . import (info,
               query,
               individuals,
               filtering_terms,
               access_levels,
               test)

routes = [
    web.get('/test'        , test.test),

    # Info
    web.get('/'            , info.handler_root),
    web.get('/info'        , info.handler_info),
    web.get('/service-info', info.handler_service_info),

    # Query
    web.get('/query'       , query.handler),

    # Individuals
    web.get('/individuals_rest', individuals.handler),
    web.get('/individuals_rest/{target_id_req}', individuals.handler),
    web.post('/individuals_rest', individuals.handler),
    web.post('/individuals_rest/{target_id_req}', individuals.handler),

    # Filtering terms
    web.get('/filtering_terms', filtering_terms.handler),

    # Filtering terms
    web.get('/access_levels', access_levels.handler),
]

