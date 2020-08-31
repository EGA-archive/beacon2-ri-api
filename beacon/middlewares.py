import base64

import aiohttp_csrf
import aiohttp_jinja2
from aiohttp import web
from cryptography import fernet
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

CSRF_FIELD_NAME = 'csrf_token'
SESSION_STORAGE = 'beacon'

@aiohttp_jinja2.template('404.html')
async def handle_404(request):
    return {
        'cookies': request.cookies
    }

@aiohttp_jinja2.template('500.html')
async def handle_500(request):
    return {
        'cookies': request.cookies
    }


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:
        if ex.status == 500:
            return await handle_500(request)
        if ex.status == 404:
            return await handle_404(request)
        raise

# @web.middleware
# async def json_middleware(request, handler):
#     data = await handler(request)
#     return await json_stream(request, data)


def setup_middlewares(app):
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



