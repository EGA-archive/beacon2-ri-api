from typing import Dict

from pymongo.cursor import Cursor
from pymongo.collection import Collection
from beacon.db import client
from beacon.request.model import RequestParams
import logging

LOG = logging.getLogger(__name__)


def query_id(query: dict, document_id) -> dict:
    query["id"] = document_id
    return query


def query_ids(query: dict, ids) -> dict:
    query["id"] = ids
    return query


def query_property(query: dict, property_id: str, value: str, property_map: Dict[str, str]) -> dict:
    query[property_map[property_id]] = value
    return query


def get_count(collection: Collection, query: dict) -> int:
    if not query:
        LOG.debug("Returning estimated count")
        return collection.estimated_document_count()
    else:
        LOG.debug("FINAL QUERY (COUNT): {}".format(query))
        LOG.debug("Returning count")
        return collection.count_documents(query)


def get_documents(collection: Collection, query: dict, skip: int, limit: int) -> Cursor:
    LOG.debug("FINAL QUERY: {}".format(query))
    return collection.find(query).skip(skip).limit(limit).max_time_ms(10 * 1000)
