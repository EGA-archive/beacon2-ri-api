from aiohttp.web_request import Request
from aiohttp import web


async def handler(request: Request):
    location = request.app.router['info'].url_for()
    raise web.HTTPFound(location=location)
