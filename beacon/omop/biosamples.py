import logging
from typing import Dict, List, Optional
from beacon.omop.filters import apply_alphanumeric_filter, apply_filters
from beacon.omop.utils import query_id, query_ids, get_count, get_documents, get_cross_query, get_filtering_documents
from beacon.omop import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.omop.filters import *
from beacon.omop.schemas import DefaultSchemas
from beacon.omop.utils import search_ontologies, basic_query
from beacon.request.model import RequestParams

import aiosql
import itertools

from pathlib import Path
queries_file = Path(__file__).parent / "sql" / "biosamples.sql"
biosamples_queries = aiosql.from_path(queries_file, "psycopg2")


LOG = logging.getLogger(__name__)

def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    include = qparams.query.include_resultset_responses
    if include == 'HIT':    # Usual query, returns what do you have
        query = query
    elif include == 'ALL':  # Return all data
        query = {}
    elif include == 'NONE': # Return 0 data
        query = {'$text': {'$search': '########'}}
    else:
        query = query
    # MISS: Return negative queries
    return query

def get_biosample_id(offset=0, limit=10, biosample_id=None):
    if biosample_id == None:
        records = biosamples_queries.sql_get_biosamples(client, offset=offset, limit=limit)
        listId = [str(record[0]) for record in records]
        LOG.debug(listId)
    else:
        records = biosamples_queries.sql_get_biosample_id(client, specimen_id=biosample_id)
        listId = [str(records[0])]
    return listId


def get_specimens(listIds):
    dict_specimens = {}
    for biosample_id in listIds:
        records = biosamples_queries.sql_get_specimen(client, specimen_id = biosample_id)
        listValues = []
        for record in records:
            listValues.append({'person_id': record[0],
                               'disease_status_concept_id': record[1],
                               'anatomic_site_concept_id': record[2],
                               'specimen_date': record[3],
                               'specimen_moment': record[4]})
        dict_specimens[biosample_id] = listValues
    return dict_specimens

def format_query(listIds, specimens):

    list_format = []
    for biosample_id in listIds:
        dict_biosample_id =  { 
            "id": str(biosample_id),
            "individualId": str(specimens[biosample_id][0]["person_id"]),
            "biosampleStatus": {
                "id":  specimens[biosample_id][0]["disease_status_concept_id"]["id"],
                "label": specimens[biosample_id][0]["disease_status_concept_id"]["label"]
            },
            "sampleOriginType": {
                "id" : specimens[biosample_id][0]["anatomic_site_concept_id"]["id"],
                "label" : specimens[biosample_id][0]["anatomic_site_concept_id"]["label"]
            },
            "collectionMoment": specimens[biosample_id][0]["specimen_date"],
            "collectionDate": specimens[biosample_id][0]["specimen_moment"],
            "info": {}
            }
        list_format.append(dict_biosample_id)
    return list_format


def map_domains(domain_id):
    # Domain_id : Table in OMOP
    # Maybe there is more than one mapping in the condition domain
    dictMapping = {
        'Spec Disease Status':'disease_status_concept_id',
        'Spec Anatomic Site':'"anatomic_site_concept_id"'
    }
    return dictMapping[domain_id]

def search_descendants(concept_id):
    records = biosamples_queries.sql_get_descendants(client, concept_id=concept_id)

    l_descendants = set()
    for descendant in records:
        l_descendants.add(descendant[0])
    return l_descendants

def create_dynamic_filter(filters):

    list_person = []
    for filter in filters:
        # Default type of filter is ontology
        filterType = 'Ontology'
        # For now there is no Alphanumeric available option
        if filter[2]:       # If filter has an operator (operator!=None) it is an Alphanumeric filter
            filterType = 'Alphanumeric'

        if "disease_status_concept_id" in filter[0] or "anatomic_site_concept_id" in filter[0]:
            variable_name = filter[0]
            list_concept_id = []
            for concept_id in filter[1]:
                list_concept_id.append(variable_name + ' = ' + str(concept_id))
            query_person_id =  ' or '.join(list_concept_id)
            list_person.append(' ( ' + query_person_id + ' ) ')

    return list_person

def super_query_count(filter):
    return  f""" select count(distinct specimen_id)
        from cdm.specimen p
        where true and
        {filter[0]}
    """

def super_query_get(filter, offset, limit):
    return  f""" select specimen_id
        from cdm.specimen p
        where true and
        {filter[0]}
        limit {limit}
        offset {offset}
    """

# Function to know if generator is empty
def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)

def checkFilters(filtersDict, offset, limit, typeQuery):
    listOfList = []
    dictTableMap = []
    for filter in filtersDict:
        listConcept_id = set()
        operator = None
        value = None
        includeDescendantTerms = True

        # Check query
        # Parse query depend on POST/GET query
        if typeQuery == 'POST':
            if 'includeDescendantTerms' in filter:
                if filter['includeDescendantTerms'] == False:
                    includeDescendantTerms = False
            if 'operator' in filter:
                operator = filter['operator']
                value = filter['value']
                includeDescendantTerms = False
            if 'id' in filter:
                filterId = filter['id']
                print(filterId)
            else:
                return [], 0
        else: # If GET
            filterId = filter

        vocabulary_id, concept_code = filterId.split(':')
        print(vocabulary_id, concept_code)
        records = biosamples_queries.sql_get_concept_domain(client,
                                                            vocabulary_id=vocabulary_id,
                                                            concept_code=concept_code)
        # Check if records is empty
        res = peek(records)
        if res is None:
            return [], 0
        _, records = res
        for record in records:
            print(record)
            original_concept_id = record[0]
            domain_id = record[1]
        listConcept_id.add(original_concept_id)
        # Look in which domains the concept_id belongs
        tableMap=map_domains(domain_id)
        if includeDescendantTerms:
            # Import descendants of the concept_id
            concept_ids= search_descendants(original_concept_id)
            # Concept_id and descendants in same set()
            listConcept_id = listConcept_id.union(concept_ids)
        dictTableMap.append([tableMap, listConcept_id, operator, value])
    base_filter = create_dynamic_filter(dictTableMap)
    query_count = super_query_count(base_filter)
    count_records = basic_query(query_count)
    query_get = super_query_get(base_filter, offset, limit)
    records_get = basic_query(query_get)
    listOfList = [str(record[0]) for record in records_get]

    return listOfList, count_records[0][0]

# /individuals/?filters=SNOMED:0&filters=OMOP:23
def filters(filtersDict, offset, limit):
    if type(filtersDict[0]) is dict:         # If filter is from Post
        listFilters, count = checkFilters(filtersDict, offset, limit, 'POST')
    else:
        listFilters, count = checkFilters(filtersDict, offset, limit, 'GET')

    return listFilters, count

def get_biosamples(entry_id: Optional[str], qparams: RequestParams):
    LOG.debug("Enter biosamples")

    schema = DefaultSchemas.BIOSAMPLES

    count_ids = 0
    if qparams.query.filters:
        listIds, count_ids = filters(qparams.query.filters,
                        offset=qparams.query.pagination.skip,
                        limit=qparams.query.pagination.limit)
        print(listIds, count_ids)
        if count_ids == 0:
            return schema, count_ids, []
    else:
        LOG.debug(entry_id)
        listIds = get_biosample_id(offset=qparams.query.pagination.skip,
                                            limit=qparams.query.pagination.limit,
                                            biosample_id=entry_id)                 # List with all Ids
        count_ids = biosamples_queries.get_count_specimen(client)   # Count specimen
        LOG.debug("com va tot")
        LOG.debug(count_ids)

    specimens = get_specimens(listIds)
    specimens = search_ontologies(specimens)
    print(specimens)

    docs = format_query(listIds, specimens)

    return schema, count_ids, docs


def get_biosample_with_id(entry_id: Optional[str], qparams: RequestParams):

    listIds = get_biosample_id(biosample_id=entry_id)

    schema = DefaultSchemas.BIOSAMPLES
    count = 1 # biosamples_queries.get_count_specimen(client)
    specimens = get_specimens(listIds)
    specimens = search_ontologies(specimens)

    docs = format_query(listIds, specimens)
    return schema, count, docs

def get_filtering_terms_of_biosample(entry_id: Optional[str], qparams: RequestParams):
    schema = DefaultSchemas.FILTERINGTERMS
    bio_filters = biosamples_queries.sql_filtering_terms_biosample(client)
    l_bioFilters = []
    for filters in bio_filters:
        if filters[0].endswith("OMOP generated"):
                continue
        dict_filter = {"id":filters[0],"label":filters[1],"scopes":["biosample"],"type":"ontology"}
        l_bioFilters.append(dict_filter)
    return schema, len(l_bioFilters), l_bioFilters
