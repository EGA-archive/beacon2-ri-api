"""
Beacon API Web Server.

Designed with async/await programming model.
"""
import logging
import os

from aiohttp import web

from . import conf, load_logger, endpoints
from .utils import db

LOG = logging.getLogger(__name__)

async def initialize(app):
    """Initialize server."""
    # Get when the data was last modified (This will also check if DB is up)
    update_datetime = (await db.get_last_modified_date()).strftime(conf.datetime_format)
    LOG.info("Update datetime: %s", update_datetime)
    setattr(conf, 'update_datetime', update_datetime)
    LOG.info("Initialization done.")

async def destroy(app):
    """Upon server close, close the DB connections."""
    LOG.info("Shutting down.")
    await db.close()

def main(path=None):
    """Run the beacon API."""

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
    if getattr(conf, 'beacon_tls_enabled', False):
        use_as_client = getattr(conf, 'beacon_tls_client', False)
        sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH if use_as_client else ssl.Purpose.SERVER_AUTH)
        sslcontext.load_cert_chain(conf.beacon_cert, conf.beacon_key) # should exist
        sslcontext.check_hostname = False
        # TODO: add the CA chain


    # .... and cue music
    if path:
        if os.path.exists(path):
            os.unlink(path)
        # will create the UDS socket and bind to it
        web.run_app(beacon, path=path, shutdown_timeout=0, ssl_context=ssl_context)
    else:
        web.run_app(beacon,
                    host=getattr(conf, 'beacon_host', '0.0.0.0'),
                    port=getattr(conf, 'beacon_port', 5050),
                    shutdown_timeout=0, ssl_context=ssl_context)


if __name__ == '__main__':

    import sys
    if len(sys.argv) > 1: # Unix socket
        main(path=sys.argv[1])
    else: # host:port
        main()
