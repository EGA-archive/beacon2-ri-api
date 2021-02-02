"""
Dummy permissions server

We hard-code the dataset permissions.

"""
import logging

from aiohttp import web

from . import load_logger
from .auth import bearer_required

# update that line to use your prefered permissions plugin
from .plugins import DummyPermissions as PermissionsProxy

LOG = logging.getLogger(__name__)

@bearer_required
async def permission(request, username):

    if request.headers.get('Content-Type') == 'application/json':
        post_data = await request.json()
        requested_datasets = post_data.get('datasets', []) # already a list
    else:
        post_data = await request.post() # request.json() crashes on empty data
        LOG.debug('POST DATA: %s', post_data)
        requested_datasets = post_data.get('datasets', '').split(',')

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
    server.add_routes([web.post('/', permission)])

    web.run_app(server,
                host='0.0.0.0',
                port=5051,
                shutdown_timeout=0, ssl_context=None)


if __name__ == '__main__':
    main()


