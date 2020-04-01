"""
Beacon API Web Server.

Server was designed with async/await mindset and with at aim at performance.
"""

from aiohttp import web
import os
import sys
import aiohttp_cors
import logging
import asyncio
import json

from .conf.config import init_db_pool
from .conf.logging import load_logger
from .schemas import load_schema
from .utils.validate import validate, parse_request_object, validate_services, parse_basic_request_object, validate_access_levels, validate_simple
from .api.exceptions import BeaconUnauthorised, BeaconBadRequest, BeaconForbidden, BeaconServerError

from .api.info import info_handler
from .api.filtering_terms import filtering_terms_handler
from .api.access_levels import access_levels_terms_handler
from .api.services import services_handler

from .api.query import query_request_handler
from .api.genomic_query import genomic_request_handler

# from .api.samples.bak import sample_request_handler
from .api.samples_ind import sample_ind_request_handler
from .api.samples_ind_rest import by_id_handler, smt_by_id

from .api.individuals_rest import get_individuals_rest



LOG = logging.getLogger(__name__)
routes = web.RouteTableDef()


# ----------------------------------------------------------------------------------------------------------------------
#                                         INFO ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------
@routes.get('/service-info')  # For GA4GH Specification
@routes.get('/')  # For Beacon API Specification
@routes.get('/info')
async def beacon_get(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of all the necessary info on the beacon and the API.

    It uses the '/' and '/service-info' path and only serves an information giver.
    """
    LOG.info('GET request to the info endpoint.')
    method, processed_request = await parse_basic_request_object(request)
    db_pool = request.app['pool']
    if str(request.rel_url) == '/service-info':
        LOG.info('Using GA4GH Discovery format for Service Info.')
        response = await info_handler(request, processed_request, db_pool, service_info=True)
    elif str(request.rel_url).startswith('/info'):    
        response = await info_handler(request, processed_request, db_pool, info_endpoint=True)
    else:
        response = await info_handler(request, processed_request, db_pool)
    return web.json_response(response)


# ----------------------------------------------------------------------------------------------------------------------
#                                         FILTERING TERMS ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------

@routes.get('/filtering_terms')  # For Beacon API Specification
async def beacon_filtering_terms(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of all the possible FILTERING TERMS in this beacon.

    It uses the '/filtering_terms' path and only serves an information giver.
    """
    LOG.info('GET request to the filtering_terms endpoint.')
    db_pool = request.app['pool']
    response = await filtering_terms_handler(request.host, db_pool)
    return web.json_response(response)


# ----------------------------------------------------------------------------------------------------------------------
#                                         ACCESS LEVELS ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------

@routes.get('/access_levels')
@validate_access_levels
async def beacon_access_levels(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of the ACCESS LEVELS.

    It uses the '/access_levels' path and only serves an information giver.
    """
    LOG.info('GET request to the access_levels endpoint.')
    db_pool = request.app['pool']
    method, processed_request = await parse_basic_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    response = await access_levels_terms_handler(db_pool, processed_request, request)
    return web.json_response(response)

@routes.post('/access_levels')
@validate_access_levels
async def beacon_post_access_levels(request):
    """Find access levels using POST endpoint."""
    LOG.info('POST request to the access_levels endpoint.')
    db_pool = request.app['pool']
    method, processed_request = await parse_basic_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    response = await access_levels_terms_handler(db_pool, processed_request, request)
    return web.json_response(response)


# ----------------------------------------------------------------------------------------------------------------------
#                                         SERVICES ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------

@routes.get('/services')
@validate_services
async def beacon_get(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of all the necessary info of the SERVICES.

    It uses the '/services' path and only serves an information giver.
    """
    LOG.info('GET request to the services endpoint.')
    db_pool = request.app['pool']
    method, processed_request = await parse_basic_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    response = await services_handler(db_pool, processed_request, request)

    return web.json_response(response, content_type='application/json', dumps=json.dumps)

@routes.post('/services')
@validate_services
async def beacon_get(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of all the necessary info of the SERVICES.

    It uses the '/services' path and only serves an information giver.
    """
    LOG.info('POST request to the services endpoint.')
    db_pool = request.app['pool']
    method, processed_request = await parse_basic_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    response = await services_handler(db_pool, processed_request, request)

    return web.json_response(response, content_type='application/json', dumps=json.dumps)


########################################################################################################################


# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------

@routes.get('/query')
@validate("query")
async def beacon_get_query(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given QUERY.

    It uses the '/query' path and expects some parameters.
    """
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    query_response = await query_request_handler(db_pool, processed_request, request)
    return web.json_response(query_response, content_type='application/json', dumps=json.dumps)



@routes.post('/query')
@validate("query")
async def beacon_post_query(request):
    """Find datasets using POST endpoint."""
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    query_response = await query_request_handler(db_pool, processed_request, request)
    return web.json_response(query_response, content_type='application/json', dumps=json.dumps)


# ----------------------------------------------------------------------------------------------------------------------
#                                         GENOMIC_SNP ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------

@routes.get('/genomic_snp')
@validate("genomic_snp")
async def beacon_get_snp(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given SNP QUERY.

    It uses the '/genomic_snp' path and expects some parameters.
    """
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    query_response = await genomic_request_handler(db_pool, processed_request, request)
    return web.json_response(query_response, content_type='application/json', dumps=json.dumps)



@routes.post('/genomic_snp')
@validate("genomic_snp")
async def beacon_post_snp(request):
    """Find datasets using POST endpoint."""
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    query_response = await genomic_request_handler(db_pool, processed_request, request)
    return web.json_response(query_response, content_type='application/json', dumps=json.dumps)


# ----------------------------------------------------------------------------------------------------------------------
#                                         GENOMIC_REGION ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------

@routes.get('/genomic_region')
@validate("genomic_region")
async def beacon_get_region(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given REGION QUERY.

    It uses the '/genomic_region' path and expects some parameters.
    """
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    query_response = await genomic_request_handler(db_pool, processed_request, request)
    return web.json_response(query_response, content_type='application/json', dumps=json.dumps)



@routes.post('/genomic_region')
@validate("genomic_region")
async def beacon_post_region(request):
    """Find datasets using POST endpoint."""
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    query_response = await genomic_request_handler(db_pool, processed_request, request)
    return web.json_response(query_response, content_type='application/json', dumps=json.dumps)


# ----------------------------------------------------------------------------------------------------------------------
#                                         gVariant ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------

@routes.get('/g_variant')
@validate("gVariant")
async def beacon_get_region(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given QUERY.

    It uses the '/g_variant' path and expects some parameters.

    Serves as an alias of /genomic_snp and /genomic_region, accepts diverse parameters
    and depending the combination uses one handler or the other. 
    """
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    # if not processed_request.get("end"):
    #     response = await snp_request_handler(db_pool, processed_request, request)
    # else: 
    #     response = await region_request_handler(db_pool, processed_request, request)
    response = await genomic_request_handler(db_pool, processed_request, request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)



@routes.post('/gVariant')
@validate("gVariant")
async def beacon_post_region(request):
    """Find datasets using POST endpoint."""
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")
    # if not processed_request.get("end"):
    #     response = await snp_request_handler(db_pool, processed_request, request)
    # else: 
    #     response = await region_request_handler(db_pool, processed_request, request)
    response = await genomic_request_handler(db_pool, processed_request, request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)


# ----------------------------------------------------------------------------------------------------------------------
#                                         SAMPLES ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------
      
@routes.get('/samples')
@validate("samples_ind")
async def beacon_get_samples_test(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given SAMPLES QUERY.

    It uses the '/samples' path and expects some parameters.
    """
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    sample_response = await sample_ind_request_handler(db_pool, processed_request, request)
    return web.json_response(sample_response, content_type='application/json', dumps=json.dumps)


@routes.post('/samples')
@validate("samples_ind")
async def beacon_get_samples_test(request):
    """Find samples using POST endpoint."""
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    sample_response = await sample_ind_request_handler(db_pool, processed_request, request)
    return web.json_response(sample_response, content_type='application/json', dumps=json.dumps)


# ----------------------------------------------------------------------------------------------------------------------
#                                         INDIVIDUAL ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------

# Note that we use the same operations that in samples since both endpoints are almost the same
@routes.get('/individuals')
@validate("samples_ind")
async def beacon_get_samples_test(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given INDIVIDUALS QUERY.

    It uses the '/individuals' path and expects some parameters.
    """
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    sample_response = await sample_ind_request_handler(db_pool, processed_request, request)
    return web.json_response(sample_response, content_type='application/json', dumps=json.dumps)


@routes.post('/individuals')
@validate("samples_ind")
async def beacon_get_samples_test(request):
    """Find individuals using POST endpoint."""
    db_pool = request.app['pool']
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    sample_response = await sample_ind_request_handler(db_pool, processed_request, request)
    return web.json_response(sample_response, content_type='application/json', dumps=json.dumps)


# ----------------------------------------------------------------------------------------------------------------------
#                                    SAMPLES/INDIVIDUALS REST ENDPOINT OPERATIONS
# ----------------------------------------------------------------------------------------------------------------------

# Individuals
## Individual by ID
@routes.get('/individuals/{target_id_req}')
@validate("samples_ind_by_id")
async def beacon_get_individual_by_id(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given INDIVIDUALS QUERY.

    It uses the '/individuals/{individual_stable_id_req}' path and doesn't expect parameters (just alternative schemas).
    """
    db_pool = request.app['pool']
    LOG.info(f"Using {request.path}")
    LOG.info(f"This is the {request.method} variable request: {request.match_info['target_id_req']}")
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    response = await by_id_handler(db_pool, request, processed_request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)

## Samples from individual by individual ID
@routes.get('/individuals/{target_id_req}/samples')
@validate("samples_ind")
async def beacon_get_individual_by_id(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given INDIVIDUALS QUERY.

    It uses the '/individuals/{individual_stable_id_req}/samples' path, it can expect parameters.
    """
    db_pool = request.app['pool']
    LOG.info(f"Using {request.path}")
    LOG.info(f"This is the {request.method} variable request: {request.match_info['target_id_req']}")
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    response = await smt_by_id(db_pool, processed_request, request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)

## Variants from individual by individual ID
@routes.get('/individuals/{target_id_req}/variants')
@validate("samples_ind")
async def beacon_get_individual_by_id(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given INDIVIDUALS QUERY.

    It uses the '/individuals/{individual_stable_id_req}/variants' path, it can expect parameters.
    """
    db_pool = request.app['pool']
    LOG.info(f"Using {request.path}")
    LOG.info(f"This is the {request.method} variable request: {request.match_info['target_id_req']}")
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    response = await smt_by_id(db_pool, processed_request, request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)


# Samples
## Sample by sample ID
@routes.get('/samples/{target_id_req}')
@validate("samples_ind_by_id")
async def beacon_get_individual_by_id(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given SAMPLES QUERY.

    It uses the '/samples/{target_id_req}' path and doesn't expect parameters.
    """

    db_pool = request.app['pool']
    LOG.info(f"Using {request.path}")
    LOG.info(f"This is the {request.method} variable request: {request.match_info['target_id_req']}")
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    response = await by_id_handler(db_pool, request, processed_request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)

## Individual from sample by sample ID
@routes.get('/samples/{target_id_req}/individuals')
@validate("samples_ind")
async def beacon_get_individual_by_id(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given SAMPLES QUERY.

    It uses the '/samples/{target_id_req}/individuals' path, it can expect parameters.
    """
    db_pool = request.app['pool']
    LOG.info(f"Using {request.path}")
    LOG.info(f"This is the {request.method} variable request: {request.match_info['target_id_req']}")
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    response = await smt_by_id(db_pool, processed_request, request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)

## Variants from sample by sample ID
@routes.get('/samples/{target_id_req}/variants')
@validate("samples_ind")
async def beacon_get_individual_by_id(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given SAMPLES QUERY.

    It uses the '/samples/{target_id_req}/variants' path, it can expect parameters.
    """
    db_pool = request.app['pool']
    LOG.info(f"Using {request.path}")
    LOG.info(f"This is the {request.method} variable request: {request.match_info['target_id_req']}")
    method, processed_request = await parse_request_object(request)
    LOG.info(f"This is the {method} processed request: {processed_request}")

    response = await smt_by_id(db_pool, processed_request, request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)


# ----------------------------------------------------------------------------------------------------------------------
#                                    REST INDIVIDUALS (FROM SCRATCH) ENDPOINT
# ----------------------------------------------------------------------------------------------------------------------

@routes.get('/individuals_rest')
@validate_simple("individuals_rest_GET")
async def beacon_get_individuals_rest(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given INDIVIDUALS QUERY.

    It uses the '/individuals' path, it can expect parameters.
    """
    db_pool = request.app['pool']
    LOG.info(f"Using {request.path}")

    response = await get_individuals_rest(db_pool, request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)

@routes.get('/individuals_rest/{target_id_req}')
@validate_simple("individuals_rest_GET")
async def beacon_get_individuals_rest(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given INDIVIDUALS QUERY.

    It uses the '/individuals' path, it can expect parameters.
    """
    db_pool = request.app['pool']
    LOG.info(f"Using {request.path}")

    response = await get_individuals_rest(db_pool, request)
    return web.json_response(response, content_type='application/json', dumps=json.dumps)

########################################################################################################################


# ----------------------------------------------------------------------------------------------------------------------
#                                         SETUP FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------


async def initialize(app):
    """Spin up DB a connection pool with the HTTP server."""
    LOG.debug('Create PostgreSQL connection pool.')
    app['pool'] = await init_db_pool()
    LOG.debug("Testing the DB connection.")
    db_pool = app['pool']
    async with db_pool.acquire(timeout=180) as connection:
        query = """SELECT 1;
                    """
        statement = await connection.prepare(query)
        db_response =  await statement.fetch()
    set_cors(app)
    LOG.info("Initialization done.")


async def destroy(app):
    """Upon server close, close the DB connection pool."""
    await app['pool'].close()


def set_cors(server):
    """Set CORS rules."""
    # Configure CORS settings
    cors = aiohttp_cors.setup(server, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    # Apply CORS to endpoints
    for route in list(server.router.routes()):
        cors.add(route)


@load_logger
def main():
    """Run the beacon API.

    At start also initialize a PostgreSQL connection pool.
    """

    beacon = web.Application()
    beacon.router.add_routes(routes)
    beacon.on_startup.append(initialize)
    beacon.on_cleanup.append(destroy)

    # TO DO make it HTTPS and request certificate
    # sslcontext.load_cert_chain(ssl_certfile, ssl_keyfile)
    # sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # sslcontext.check_hostname = False
    web.run_app(beacon, host=os.environ.get('HOST', '0.0.0.0'),
                port=os.environ.get('PORT', '5050'),
                shutdown_timeout=0, ssl_context=None)




if __name__ == '__main__':
    if sys.version_info < (3, 6):
        LOG.error("beacon-python requires python3.6")
        sys.exit(1)
    main()
