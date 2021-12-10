from collections import defaultdict
from typing import List, Union
import re
import dataclasses

from beacon.request.model import AlphanumericFilter, CustomFilter, OntologyFilter

import logging

LOG = logging.getLogger(__name__)

CURIE_REGEX = r'^([a-zA-Z0-9]*):\/?[a-zA-Z0-9]*$'


def dataclass_from_dict(klass, d):
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(klass)}
        return klass(**{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d})
    except:
        return d


def apply_filters(query: dict, filters: List[Union[OntologyFilter, AlphanumericFilter, CustomFilter]]) -> dict:
    if len(filters) > 0:
        query["$text"] = defaultdict(str)
    for filter in filters:
        if "value" in filter:
            LOG.debug("Alphanumeric filter: %s %s %s", filter["id"], filter["operator"], filter["value"])
            filter = dataclass_from_dict(AlphanumericFilter, filter)
            query = apply_alphanumeric_filter(query, filter)
        elif "similarity" in filter or "include_descendant_terms" in filter or re.match(CURIE_REGEX, filter["id"]):
            LOG.debug("Ontology filter: %s", filter["id"])
            filter = dataclass_from_dict(OntologyFilter, filter)
            query = apply_ontology_filter(query, filter)
        else:
            LOG.debug("Custom filter: %s", filter["id"])
            filter = dataclass_from_dict(CustomFilter, filter)
            query = apply_custom_filter(query, filter)
    return query


def apply_ontology_filter(query: dict, filter: OntologyFilter) -> dict:
    # TODO: Add descendants
    # TODO: Similarity
    if query["$text"]["$search"]:
        query["$text"]["$search"] += " "
    query["$text"]["$search"] += '\"' + filter.id + '\"'
    LOG.debug("QUERY: %s", query)
    return query


def apply_alphanumeric_filter(query: dict, filter: AlphanumericFilter) -> dict:
    if filter.value.isnumeric():
        if float(filter.value).is_integer:
            query[filter.id] = int(filter.value)
        else:
            query[filter.id] = float(filter.value)
    else:
        query[filter.id] = filter.value
    
    LOG.debug("QUERY: %s", query)
    return query


def apply_custom_filter(query: dict, filter: CustomFilter) -> dict:
    if query["$text"]["$search"]:
        query["$text"]["$search"] += " "
    query["$text"]["$search"] += filter.id
    LOG.debug("QUERY: %s", query)
    return query
