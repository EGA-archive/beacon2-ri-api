import aiohttp_csrf
import aiohttp_jinja2
from aiohttp import web

@aiohttp_jinja2.template('404.html')
async def handle_404(request):
    return {}
@aiohttp_jinja2.template('500.html')
async def handle_500(request):
    return {}




@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status == 500:
            return await handle_500(request)
        if response.status == 404:
            return await handle_404(request)
        return response
    except web.HTTPException as ex:
        if response.status == 500:
            return await handle_500(request)
        if response.status == 404:
            return await handle_404(request)
        raise


CSRF_FIELD_NAME = 'csrf_token'
CSRF_COOKIE_NAME = 'csrf_token'

def setup_middlewares(app):
    # CSRF middleware
    aiohttp_csrf.setup(app,
                       policy=aiohttp_csrf.policy.FormPolicy(CSRF_FIELD_NAME),
                       storage=aiohttp_csrf.storage.CookieStorage(CSRF_COOKIE_NAME))
    app.middlewares.append(aiohttp_csrf.csrf_middleware)

    # Capture 404 and 500
    app.middlewares.append(error_middleware)

