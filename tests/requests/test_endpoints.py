import os
import ssl
from beacon import __main__
from aiohttp import web
from aiohttp_middlewares import cors_middleware
from beacon.response import middlewares
from beacon.request.routes import routes
from pathlib import Path


def create_app():
    beacon = web.Application(
        middlewares=[web.normalize_path_middleware(), middlewares.error_middleware, cors_middleware(origins=["https://beacon-network-test.ega-archive.org", "https://beacon-network-test2.ega-archive.org", "https://beacon-network-demo.ega-archive.org","https://beacon-network-demo2.ega-archive.org", "http://localhost:3000", "http://localhost:3010", "https://beacon-network-cineca-demo.ega-archive.org"])]
    )
    beacon.add_routes(routes)
    return beacon

async def test_get_individuals(aiohttp_client):
    beacon_client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    resp = await beacon_client.get("/api/individuals")
    assert resp.status == 200

async def test_post_individuals(aiohttp_client):
    beacon_client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    request_body=b'{"meta": { \
    "apiVersion": "2.0" \
        }, \
        "query": { \
            "filters": [ \
    {"id": "NCIT:C16576"}], \
            "includeResultsetResponses": "HIT", \
            "pagination": { \
                "skip": 0, \
                "limit": 10 \
            }, \
            "testMode": false, \
            "requestedGranularity": "record" \
        } \
    }'
    resp = await beacon_client.post("/api/individuals", data=request_body)
    assert resp.status == 200

async def test_get_g_variants(aiohttp_client):
    beacon_client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    resp = await beacon_client.get("/api/g_variants")
    assert resp.status == 200

async def test_post_g_variants(aiohttp_client):
    beacon_client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    request_body=b'{"meta": { \
        "apiVersion": "2.0" \
    }, \
    "query": { \
        "requestParameters": { \
    "alternateBases": "G" , \
    "referenceBases": "A" , \
	    "variantType": "SNP" \
        }, \
        "filters": [], \
        "includeResultsetResponses": "HIT", \
        "pagination": { \
            "skip": 0, \
            "limit": 10 \
        }, \
        "testMode": false, \
        "requestedGranularity": "record" \
    } \
    }'
    resp = await beacon_client.post("/api/g_variants", data=request_body)
    assert resp.status == 200

async def test_get_analyses(aiohttp_client):
    beacon_client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    resp = await beacon_client.get("/api/analyses")
    assert resp.status == 200

async def test_get_biosamples(aiohttp_client):
    beacon_client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    resp = await beacon_client.get("/api/biosamples")
    assert resp.status == 200

async def test_get_cohorts(aiohttp_client):
    beacon_client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    resp = await beacon_client.get("/api/cohorts")
    assert resp.status == 200

async def test_get_datasets(aiohttp_client):
    beacon_client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    resp = await beacon_client.get("/api/datasets")
    assert resp.status == 200

async def test_get_runs(aiohttp_client):
    beacon_client = await aiohttp_client(create_app(), server_kwargs={'port': 5050})
    resp = await beacon_client.get("/api/runs")
    assert resp.status == 200
