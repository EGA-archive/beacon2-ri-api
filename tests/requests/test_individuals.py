import os
import ssl
from beacon import __main__
from aiohttp import web
from aiohttp_middlewares import cors_middleware
from beacon.response import middlewares
from beacon.request.routes import routes
from pathlib import Path
from beacon import conf


def create_app():
    beacon = web.Application(
        middlewares=[web.normalize_path_middleware(), middlewares.error_middleware, cors_middleware(origins=["https://beacon-network-test.ega-archive.org", "https://beacon-network-test2.ega-archive.org", "https://beacon-network-demo.ega-archive.org","https://beacon-network-demo2.ega-archive.org", "http://localhost:3000", "http://localhost:3010", "https://beacon-network-cineca-demo.ega-archive.org"])]
    )
    beacon.add_routes(routes)
    path=None
    ssl_context = None
    return beacon

async def test_get_individuals(aiohttp_client):
    client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    resp = await client.get("/api")
    assert resp.status == 200