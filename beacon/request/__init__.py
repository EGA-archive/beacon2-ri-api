import json
from dataclasses import dataclass
from enum import Enum
from typing import List
from dataclasses_json import dataclass_json, LetterCase
from aiohttp.web_request import Request
from beacon.request.model import IncludeResultsetResponses, RequestParams, RequestMeta, RequestQuery, Pagination
from beacon import conf

import logging

LOG = logging.getLogger(__name__)


async def get_parameters(request: Request) -> RequestParams:
    if request.method == "POST" and request.has_body and request.can_read_body:
        params = RequestParams.from_json(await request.content.read(-1))
        LOG.debug(params)
        return params
    else:
        requested_schema: str = request.query.get("requestedSchema", "")
        skip: int = int(request.query.get("skip", 0))
        limit: int = int(request.query.get("limit", 10))
        include_resultset_responses: IncludeResultsetResponses = \
            IncludeResultsetResponses(request.query.get("includeResultsetResponses", "HIT"))
        return RequestParams(
            RequestMeta([requested_schema] if requested_schema else []),
            RequestQuery(
                include_resultset_responses=include_resultset_responses,
                pagination=Pagination(skip, limit)
            )
        )
