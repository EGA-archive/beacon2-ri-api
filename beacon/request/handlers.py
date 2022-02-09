import json
import logging
from aiohttp import web
from aiohttp.web_request import Request
from bson import json_util

from beacon.request import get_parameters
from beacon.response.build_response import (
    build_beacon_resultset_response,
    build_beacon_collection_response,
    build_beacon_boolean_response,
    build_beacon_count_response,
    build_filtering_terms_response,
)
from beacon.utils.stream import json_stream

LOG = logging.getLogger(__name__)


def collection_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        LOG.debug(type(request))
        qparams = await get_parameters(request)
        entry_id = request.match_info["id"] if "id" in request.match_info else None

        # Get response
        entity_schema, records = db_fn(entry_id, qparams)
        response_converted = (
            [json.loads(json_util.dumps(r)) for r in records] if records else []
        )
        response = build_beacon_collection_response(
            response_converted, len(response_converted), qparams, lambda x, y: x, entity_schema
        )
        return await json_stream(request, response)

    return wrapper


def generic_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        LOG.debug(type(request))
        qparams = await get_parameters(request)
        entry_id = request.match_info["id"] if "id" in request.match_info else None

        # Get response
        entity_schema, records = db_fn(entry_id, qparams)
        response_converted = (
            [json.loads(json_util.dumps(r)) for r in records] if records else []
        )

        response = None
        if qparams.query.requested_granularity == "boolean":
            response = build_beacon_boolean_response(response_converted, len(response_converted), qparams, lambda x, y: x, entity_schema)
        elif qparams.query.requested_granularity == "count":
            response = build_beacon_count_response(response_converted, len(response_converted), qparams, lambda x, y: x, entity_schema)
        else:
            response = build_beacon_resultset_response(response_converted, len(response_converted), qparams, lambda x, y: x, entity_schema)
        return await json_stream(request, response)

    return wrapper

def filtering_terms_handler(db_fn, request=None):
    async def wrapper(request: Request):
        # Get params
        LOG.debug(type(request))
        qparams = await get_parameters(request)
        entry_id = request.match_info["id"] if "id" in request.match_info else None

        # Get response
        _, records = db_fn(entry_id, qparams)
        response_converted = (
            [json.loads(json_util.dumps(r)) for r in records] if records else []
        )
        resources = ontologies.get_resources()
        response = build_filtering_terms_response(response_converted, resources, qparams)
        return await json_stream(request, response)

    return wrapper
