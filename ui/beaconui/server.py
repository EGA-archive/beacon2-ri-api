#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging.config import dictConfig
import ssl
from pathlib import Path
import asyncio
from urllib.parse import urlencode
import yaml
import base64

from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import jinja2
import aiohttp_jinja2

from . import urls

LOG = logging.getLogger(__name__)

####################################

from django import setup as django_setup
django_setup()

####################################

def main(args=None):

    main_dir = Path(__file__).parent.parent.resolve()
    with open(main_dir / 'logger.yaml', 'r') as stream:
        dictConfig(yaml.load(stream))

    host = '0.0.0.0'
    port = 8000
    sslcontext = None

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    server = web.Application()
    server.router.add_get( '/'      , urls.index, name='index')
    server.router.add_get( '/login' , urls.login, name='login')
    #server.router.add_post('/query' , urls.query, name='query')

    # Where the templates are
    template_loader = jinja2.FileSystemLoader(str(main_dir / 'templates'))
    aiohttp_jinja2.setup(server, loader=template_loader)

    # Session middleware
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key) # 32 url-safe base64-encoded bytes
    session_setup(server, EncryptedCookieStorage(secret_key))

    # ...and cue music
    LOG.info(f"Start BeaconUI server on {host}:{port}")
    web.run_app(server, host=host, port=port, shutdown_timeout=0, ssl_context=sslcontext)

if __name__ == '__main__':
    main()


