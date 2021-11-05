
from typing import Dict


def query_id(query: dict, id) -> dict:
    query["id"] = id
    return query

def query_ids(query: dict, ids) -> dict:
    query["id"] = ids
    return query

def query_property(query: dict, property: str, value: str, property_map: Dict[str, str]):
    query[property_map[property]] = value