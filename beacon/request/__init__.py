from aiohttp.web_request import Request
from beacon.request.model import IncludeResultsetResponses, RequestParams

import logging

LOG = logging.getLogger(__name__)


async def get_parameters(request: Request) -> RequestParams:
    if request.method == "POST" and request.has_body and request.can_read_body:
        params = RequestParams.from_json(await request.content.read(-1))
        LOG.debug(params)
        return params
    else:
        params = RequestParams()
        for k, v in request.query.items():
            if k == "requestedSchema":
                params.meta.requested_schemas = [v]
            elif k == "skip":
                params.query.pagination.skip = int(v)
            elif k == "limit":
                params.query.pagination.limit = int(v)
            elif k == "includeResultsetResponses":
                params.query.include_resultset_responses = IncludeResultsetResponses(v)
            else:
                params.query.request_parameters[k] = v
        LOG.debug(params)
        return params
