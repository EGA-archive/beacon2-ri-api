"""
Beacon API Web Server.

Designed with async/await programming model.
"""
import logging

from aiohttp import web
import aiohttp_cors

from . import conf, load_logger, endpoints
from .api.db import pool

LOG = logging.getLogger(__name__)

async def initialize(app):
    """Initialize HTTP server."""

    # Configure CORS settings
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    # Apply CORS to endpoints
    for route in list(app.router.routes()):
        cors.add(route)

    LOG.info("Initialization done.")

async def destroy(app):
    """Upon server close, close the DB connection pool."""
    LOG.info("Shutting down.")
    await pool.close()

def main():
    """Run the beacon API.

    At start also initialize a PostgreSQL connection pool.
    """

    # Configure the logging
    load_logger()
    
    # Configure the beacon
    beacon = web.Application()
    beacon.on_startup.append(initialize)
    beacon.on_cleanup.append(destroy)

    # Configure the endpoints
    beacon.add_routes(endpoints.routes)

    # Configure HTTPS (or not)
    ssl_context = None
    if getattr(conf, 'tls_enabled', False):
        sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        sslcontext.load_cert_chain(conf.beacon_cert, conf.beacon_key)
        sslcontext.check_hostname = False
        # TODO: add the CA chain

    # .... and cue music
    web.run_app(beacon,
                host=getattr(conf, 'beacon_host', '0.0.0.0'),
                port=getattr(conf, 'beacon_port', 5050),
                shutdown_timeout=0, ssl_context=None)

