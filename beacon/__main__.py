import base64
import logging
import os
import ssl
import sys
from pathlib import Path
from time import strftime
from datetime import datetime

import aiohttp_jinja2
import jinja2
from aiohttp import web
import aiohttp_cors
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
from aiohttp_middlewares import cors_middleware
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS

from beacon import conf, load_logger
from beacon.request import ontologies
from beacon.response import middlewares
from beacon.request.routes import routes
from beacon.db import client

LOG = logging.getLogger(__name__)


async def initialize(app):
    # Load static
    app["static_root_url"] = "/static"

    # Configure jinja
    env = aiohttp_jinja2.get_env(app)
    env.globals.update(
        len=len,
        max=max,
        enumerate=enumerate,
        range=range,
        conf=conf,
        now=strftime("%Y"),
    )

    setattr(conf, 'update_datetime', datetime.now().isoformat())

    LOG.info("Initialization done.")


async def destroy(app):
    """Upon server close, close the DB connections."""
    LOG.info("Shutting down.")
    client.close()


def main(path=None):
    # Configure the logging
    load_logger()

    # Configure the beacon
    #beacon = web.Application(
        #middlewares=[web.normalize_path_middleware(), middlewares.error_middleware, cors_middleware(allow_all=True)]
    #)

    beacon = web.Application(
        middlewares=[web.normalize_path_middleware(), middlewares.error_middleware, cors_middleware(origins=["https://beacon-network-test.ega-archive.org", "https://beacon-network-test2.ega-archive.org", "https://beacon-network-demo.ega-archive.org","https://beacon-network-demo2.ega-archive.org", "http://localhost:3000", "http://localhost:3010", "https://beacon-network-cineca-demo.ega-archive.org"])]
    )


    beacon.on_startup.append(initialize)
    beacon.on_cleanup.append(destroy)

    # Prepare for the UI
    main_dir = Path(__file__).parent.parent.resolve()
    # Where the templates are
    template_loader = jinja2.FileSystemLoader(str(main_dir / "ui" / "templates"))
    aiohttp_jinja2.setup(beacon, loader=template_loader)

    # Session middleware
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(
        fernet_key
    )  # 32 url-safe base64-encoded bytes
    storage = EncryptedCookieStorage(
        secret_key, cookie_name=middlewares.SESSION_STORAGE
    )
    session_setup(beacon, storage)

    # Configure the endpoints
    beacon.add_routes(routes)



    cors = aiohttp_cors.setup(beacon, defaults={
    "https://beacon-network-test.ega-archive.org": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_methods=("POST", "PATCH", "GET", "OPTIONS"),
            allow_headers=DEFAULT_ALLOW_HEADERS
        )
})


    for route in list(beacon.router.routes()):
        cors.add(route, {
        "http://localhost:3000":
            aiohttp_cors.ResourceOptions(allow_credentials=True,
            expose_headers="*",
            allow_methods=("POST", "PATCH", "GET", "OPTIONS"),
            allow_headers=DEFAULT_ALLOW_HEADERS),
        "http://localhost:3010":
            aiohttp_cors.ResourceOptions(allow_credentials=True,
            expose_headers="*",
            allow_methods=("POST", "PATCH", "GET", "OPTIONS"),
            allow_headers=DEFAULT_ALLOW_HEADERS),
        "https://beacon-network-test2.ega-archive.org":
            aiohttp_cors.ResourceOptions(allow_credentials=True,
            expose_headers="*",
            allow_methods=("POST", "PATCH", "GET", "OPTIONS"),
            allow_headers=DEFAULT_ALLOW_HEADERS),
        "https://beacon-network-demo.ega-archive.org":
            aiohttp_cors.ResourceOptions(allow_credentials=True,
            expose_headers="*",
            allow_methods=("POST", "PATCH", "GET", "OPTIONS"),
            allow_headers=DEFAULT_ALLOW_HEADERS),
        "https://beacon-network-demo2.ega-archive.org":
            aiohttp_cors.ResourceOptions(allow_credentials=True,
            expose_headers="*",
            allow_methods=("POST", "PATCH", "GET", "OPTIONS"),
            allow_headers=DEFAULT_ALLOW_HEADERS),
        "https://beacon-network-cineca-demo.ega-archive.org":
            aiohttp_cors.ResourceOptions(allow_credentials=True,
            expose_headers="*",
            allow_methods=("POST", "PATCH", "GET", "OPTIONS"),
            allow_headers=DEFAULT_ALLOW_HEADERS)
    })

    # Configure HTTPS (or not)
    ssl_context = None
    if getattr(conf, "beacon_tls_enabled", False):
        use_as_client = getattr(conf, "beacon_tls_client", False)
        sslcontext = ssl.create_default_context(
            ssl.Purpose.CLIENT_AUTH if use_as_client else ssl.Purpose.SERVER_AUTH
        )
        sslcontext.load_cert_chain(conf.beacon_cert, conf.beacon_key)  # should exist
        sslcontext.check_hostname = False
        # TODO: add the CA chain

    # Load ontologies
    #LOG.info("Loading ontologies... (this might take a while)")
    #ontologies.load_obo()
    #LOG.info("Finished loading the ontologies...")

    # Run beacon
    if path:
        if os.path.exists(path):
            os.unlink(path)
        # will create the UDS socket and bind to it
        web.run_app(beacon, path=path, shutdown_timeout=0, ssl_context=ssl_context)
    else:
        static_files = Path(__file__).parent.parent.resolve() / "ui" / "static"
        beacon.add_routes([web.static("/static", str(static_files))])
        web.run_app(
            beacon,
            host=getattr(conf, "beacon_host", "0.0.0.0"),
            port=getattr(conf, "beacon_port", 5050),
            shutdown_timeout=0,
            ssl_context=ssl_context,
        )


if __name__ == "__main__":
    # Unix socket
    if len(sys.argv) > 1:
        main(path=sys.argv[1])
    # host:port
    else:
        main()

