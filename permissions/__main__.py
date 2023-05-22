"""
Dummy permissions server

We hard-code the dataset permissions.

"""
import logging
from typing import Optional

from aiohttp import web
from aiohttp.web import FileField
from aiohttp.web_request import Request
import aiohttp_cors
from aiohttp_middlewares import cors_middleware
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS

from . import load_logger
from .auth import bearer_required
# update that line to use your prefered permissions plugin
from .plugins import DummyPermissions as PermissionsProxy

LOG = logging.getLogger(__name__)

@bearer_required
async def permission(request: Request, username: Optional[str]):

    if request.headers.get('Content-Type') == 'application/json':
        post_data = await request.json()
    else:
        post_data = await request.post()
    LOG.debug('POST DATA: %s', post_data)

    v = post_data.get('datasets')
    if v is None:
        requested_datasets = []
    elif isinstance(v, list):
        requested_datasets = v
    elif isinstance(v, FileField):
        requested_datasets = []
    else:
        requested_datasets = v.split(sep=',')  # type: ignore
        
    LOG.debug('requested datasets: %s', requested_datasets)
    datasets = await request.app['permissions'].get(username, requested_datasets=requested_datasets)
    LOG.debug('selected datasets: %s', datasets)

    return web.json_response(list(datasets or [])) # cuz python-json doesn't like sets

async def initialize(app):
    """Initialize server."""
    app['permissions'] = PermissionsProxy()
    await app['permissions'].initialize()
    LOG.info("Initialization done.")

async def destroy(app):
    """Upon server close, close the DB connections."""
    LOG.info("Shutting down.")
    await app['permissions'].close()
    

def main(path=None):

    load_logger()

    # Configure the permissions server
    server = web.Application()
    server.on_startup.append(initialize)
    server.on_cleanup.append(destroy)

    
    # Configure the endpoints
    server.add_routes([web.post('/', permission)]) # type: ignore

    cors = aiohttp_cors.setup(server, defaults={
    "http://localhost:3000": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_methods=("POST", "PATCH", "GET", "OPTIONS"),
            allow_headers=DEFAULT_ALLOW_HEADERS
        )
})
    
    for route in list(server.router.routes()):
        cors.add(route)

    web.run_app(server,
                host='0.0.0.0',
                port=5051,
                shutdown_timeout=0, ssl_context=None)

if __name__ == '__main__':
    main()


