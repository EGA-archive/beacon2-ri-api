import logging
import base64
import json

import aiohttp_csrf
import aiohttp_jinja2
from aiohttp import web
from cryptography import fernet
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp.web import json_response

LOG = logging.getLogger(__name__)

CSRF_FIELD_NAME = 'csrf_token'
SESSION_STORAGE = 'beacon'

error_templates = {
    404: '404.html',
    500: '500.html',
}

default_errors = {
    404: 'This URL does not exist',
    500: 'Server Error',
}

def handle_error(request, exc):
    # exc is a web.HTTPException
    
    template = error_templates.get(exc.status)
    if not template:
        raise exc # We don't handle it

    context = {
        'cookies': request.cookies,
        'exception': exc
    }
    return aiohttp_jinja2.render_template(template,
                                          request,
                                          context)


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:

        # if the request comes from /api/*, we output the json version
        LOG.info('Error on page: %s', request.path)
        if request.path.startswith('/api'):
            # if it has a _beacon_response field, it's raised by the beacon
            beacon_response = getattr(ex, '_beacon_response', None)
            if not beacon_response:
                beacon_response = {
                    'error': ex.status,
                    'errorMessage': default_errors.get(ex.status)
                }
            raise web.HTTPException(text=json.dumps(beacon_response),
                                    headers = { 'Content-Type': 'application/json' }) from ex

        # Else, we are a regular HTML response
        return handle_error(request, ex)

# @web.middleware
# async def json_middleware(request, handler):
#     data = await handler(request)
#     return await json_stream(request, data)


def setup(app):
    # Session middleware
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key) # 32 url-safe base64-encoded bytes
    session_setup(app, EncryptedCookieStorage(secret_key))

    # CSRF middleware
    aiohttp_csrf.setup(app,
                       policy=aiohttp_csrf.policy.FormPolicy(CSRF_FIELD_NAME),
                       storage=aiohttp_csrf.storage.SessionStorage(SESSION_STORAGE))
    app.middlewares.append(aiohttp_csrf.csrf_middleware)


    # Capture 404 and 500
    app.middlewares.append(error_middleware)



