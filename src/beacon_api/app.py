"""
Beacon API Web Server.

Designed with async/await programming model.
"""

import sys
if sys.version_info < (3, 6):
    print("beacon-python requires python3.6", file=sys.stderr)
    sys.exit(1)

import logging
from logging.config import dictConfig
from pathlib import Path
import yaml
import os
import asyncpg

from aiohttp import web
import aiohttp_cors

from . import conf
from .endpoints import info, test


LOG = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
#                                         SETUP FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------

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

async def initialize(app):
    """Spin up DB a connection pool with the HTTP server."""
    LOG.debug('Create PostgreSQL connection pool.')
    db_pool = await asyncpg.create_pool(host=conf.database_url,
                                        port=conf.database_port,
                                        user=conf.database_user,
                                        password=conf.database_password,
                                        database=conf.database_name,
                                        server_settings={'search_path': conf.database_schema},
                                        # min_size=0, # initializing with 0 connections allows the web server to
                                                      # start and also continue to live
                                        max_queries=getattr(conf, 'database_max_queries', 50000),
                                        max_size=20, # for now limiting the number of connections in the pool
                                        timeout=getattr(conf, 'database_timeout', 120),
                                        command_timeout=getattr(conf, 'database_command_timeout', 180),
                                        max_cached_statement_lifetime=0,
                                        max_inactive_connection_lifetime=180)
    
    LOG.debug("Testing the DB connection.") # let it crash if it fails
    async with db_pool.acquire() as connection:
        _ = await connection.fetch("SELECT 1;")
    app['db_pool'] = db_pool

    set_cors(app)
    LOG.info("Initialization done.")

async def destroy(app):
    """Upon server close, close the DB connection pool."""
    await app['pool'].close()


# ----------------------------------------------------------------------------------------------------------------------
#                               .... and cue music
# ----------------------------------------------------------------------------------------------------------------------

def main():
    """Run the beacon API.

    At start also initialize a PostgreSQL connection pool.
    """

    # Configure the logging
    log_file =  Path(__file__).parent / "logger.yml"
    with open(log_file, 'r') as stream:
        dictConfig(yaml.safe_load(stream))
    
    # Configure the beacon
    beacon = web.Application()
    beacon.on_startup.append(initialize)
    beacon.on_cleanup.append(destroy)

    # Configure the endpoints
    endpoints = [
        web.get('/test'        , test.test),
        web.get('/'            , info.handler_root),
        web.get('/info'        , info.handler_info),
        web.get('/service-info', info.handler_service_info),
    ]
    beacon.add_routes(endpoints)

    # TO DO make it HTTPS and request certificate
    # sslcontext.load_cert_chain(ssl_certfile, ssl_keyfile)
    # sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # sslcontext.check_hostname = False
    web.run_app(beacon,
                host=getattr(conf, 'beacon_host', '0.0.0.0'),
                port=getattr(conf, 'beacon_PORT', 5050),
                shutdown_timeout=0, ssl_context=None)

