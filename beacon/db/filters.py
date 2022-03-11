from collections import defaultdict
from typing import List, Union
import re
import dataclasses

from beacon.request import ontologies
from beacon.request.model import AlphanumericFilter, CustomFilter, OntologyFilter

import logging

LOG = logging.getLogger(__name__)

CURIE_REGEX = r'^([a-zA-Z0-9]*):\/?[a-zA-Z0-9]*$'


def apply_filters(query: dict, filters: List[dict]) -> dict:
    if len(filters) > 0:
        query["$text"] = defaultdict(str)
    for filter in filters:
        if "value" in filter:
            filter = AlphanumericFilter(**filter)
            LOG.debug("Alphanumeric filter: %s %s %s", filter.id, filter.operator, filter.value)
            query = apply_alphanumeric_filter(query, filter)
        elif "similarity" in filter or "includeDescendantTerms" in filter or re.match(CURIE_REGEX, filter["id"]):
            filter = OntologyFilter(**filter)
            LOG.debug("Ontology filter: %s", filter.id)
            query = apply_ontology_filter(query, filter)
        else:
            filter = CustomFilter(**filter)
            LOG.debug("Custom filter: %s", filter.id)
            query = apply_custom_filter(query, filter)
    return query


def apply_ontology_filter(query: dict, filter: OntologyFilter) -> dict:
    
    # TODO: Similarity
    if query["$text"]["$search"]:
        query["$text"]["$search"] += " "
    query["$text"]["$search"] += '\"' + filter.id + '\"'

    # Apply descendant terms
    if filter.include_descendant_terms:
        descendants = ontologies.get_descendants(filter.id)
        LOG.debug("Descendants: {}".format(descendants))
        for descendant in descendants:
            descendant_filter = OntologyFilter(
                id=descendant,
                scope=filter.scope,
                include_descendant_terms=False,
                similarity=filter.similarity
            )
            query = apply_ontology_filter(query, descendant_filter)

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
