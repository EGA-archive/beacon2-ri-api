"""
Beacon API Web Server.

Designed with async/await programming model.
"""
import logging
import os
from pathlib import Path
from time import strftime

from aiohttp import web
import aiohttp_jinja2
import jinja2
from cryptography import fernet
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import base64

from . import conf, load_logger, endpoints
from .utils import db

LOG = logging.getLogger(__name__)

async def initialize(app):
    """Initialize server."""
    # Get when the data was last modified (This will also check if DB is up)
    update_datetime = (await db.get_last_modified_date()).strftime(conf.datetime_format)
    LOG.info("Update datetime: %s", update_datetime)
    setattr(conf, 'update_datetime', update_datetime)

    app['static_root_url'] = '/static'

    env = aiohttp_jinja2.get_env(app)
    #update_datetime_formatted = (await get_last_modified_date()).strftime(conf.update_datetime)
    env.globals.update(
        len=len,
        max=max,
        enumerate=enumerate,
        range=range,
        conf=conf,
        now=strftime("%Y"),
        #nsamples=await get_nsamples(),
        #update_datetime=update_datetime_formatted,
    )

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

    # Prepare for the UI
    main_dir = Path(__file__).parent.parent.resolve()
    # Where the templates are
    template_loader = jinja2.FileSystemLoader(str(main_dir / 'templates'))
    aiohttp_jinja2.setup(beacon, loader=template_loader)

    # Session middleware
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key) # 32 url-safe base64-encoded bytes
    session_setup(beacon, EncryptedCookieStorage(secret_key))

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
        static_files = Path(__file__).parent.parent.resolve() / 'static'
        beacon.add_routes([web.static('/static', str(static_files))])
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
