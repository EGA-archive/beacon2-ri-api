import logging
from typing import Dict, List, Optional
from beacon.omop.filters import apply_alphanumeric_filter, apply_filters
from beacon.omop.utils import query_id, query_ids, get_count, get_documents, get_cross_query, get_filtering_documents, search_ontologies, basic_query
from beacon.omop import client
from beacon.request.model import AlphanumericFilter, Operator, RequestParams
from beacon.omop.schemas import DefaultSchemas
from beacon.omop.utils import query_id, get_count, get_documents
from beacon.request.model import RequestParams
import json
from bson import json_util

from beacon.omop.mappings import diseases_table_map, procedures_table_map, measures_table_map, exposures_table_map

import re
import aiosql
import itertools

LOG = logging.getLogger(__name__)

from beacon.omop.utils import CDM_SCHEMA, VOCABULARIES_SCHEMA
# from beacon.omop.biosamples import get_biosamples_with_person_id
from pathlib import Path
queries_file = Path(__file__).parent / "sql" / "individuals.sql"
individual_queries = aiosql.from_path(queries_file, "psycopg2")

def include_resultset_responses(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Include Resultset Responses = {}".format(qparams.query.include_resultset_responses))
    include = qparams.query.include_resultset_responses
    if include == 'HIT':
        query = query
    elif include == 'ALL':
        query = {}
    elif include == 'NONE':
        query = {'$text': {'$search': '########'}}
    else:
        query = query
    return query

def apply_request_parameters(query: Dict[str, List[dict]], qparams: RequestParams):
    LOG.debug("Request parameters len = {}".format(len(qparams.query.request_parameters)))
    query_2={}
    for k, v in qparams.query.request_parameters.items():
        LOG.debug(k)
        
        if k == 'filters':
            if 'genomicVariations' in v:
                LOG.debug("yes")
                listing = v.split('"')
                value_list = listing[1].split('.')
                value_equal = value_list[1]
                final_list = value_equal.split('=')
                final_value = final_list[1]
                query["$and"] = []
                collection = 'g_variants'
                query["$and"].append(apply_alphanumeric_filter({}, AlphanumericFilter(
                    id=VARIANTS_PROPERTY_MAP[final_list[0]],
                    value=final_value
                ), collection))
                count = get_count(client.beacon.genomicVariations, query)
                docs = get_documents(
                client.beacon.genomicVariations,
                query,
                qparams.query.pagination.skip,
                count
            )
                biosample_IDS =[]

                query_2["$or"] = []
                for doc in docs:
                    caseLevelData = doc['caseLevelData']
                    for case in caseLevelData:
                        #LOG.debug(case["biosampleId"])
                        if case["biosampleId"] not in biosample_IDS:
                            biosample_IDS.append(case["biosampleId"])
                            query_2["$or"].append({'id': case["biosampleId"]})

                LOG.debug(query_2)
                        
                

        
    return query_2

def get_individual_id(offset=0, limit=10, person_id=None):
    if person_id == None:
        records = individual_queries.sql_get_individuals(client, offset=offset, limit=limit)
        listId = [str(record[0]) for record in records]
    else:
        records = individual_queries.sql_get_individual_id(client, person_id=person_id)
        listId = [str(records[0])]
    return listId

def get_individuals_person(listIds):
    dict_person = {}
    for person_id in listIds:
        records = individual_queries.sql_get_person(client, person_id=person_id)
        listValues = []
        for record in records:
            listValues.append({"gender_concept_id" : record[0],
                                "race_concept_id" : record[1]})
        dict_person[person_id] = listValues
    return dict_person


def get_individuals_condition(listIds):
    dict_condition = {}
    for person_id in listIds:
        records = individual_queries.sql_get_condition(client, person_id=person_id)
        listValues = []
        for record in records:
            listValues.append({"condition_concept_id" : record[0],
                               "condition_ageOfOnset" : f"P{record[1]}Y"})
        dict_condition[person_id] = listValues

    return dict_condition

def get_individuals_procedure(listIds):
    dict_procedure = {}
    for person_id in listIds:
        records = individual_queries.sql_get_procedure(client, person_id=person_id)
        listValues = []
        for record in records:
            listValues.append({"procedure_concept_id" : record[0],
                                "procedure_ageOfOnset" : f"P{record[1]}Y",
                                "procedure_date" : record[2]})
        dict_procedure[person_id] = listValues
    return dict_procedure        


def get_individuals_measures(listIds):
    dict_measures = {}
    for person_id in listIds:
        records = individual_queries.sql_get_measure(client, person_id=person_id)
        listValues = []
        for record in records:
            listValues.append({"measurement_concept_id" : record[0],
                                "measurement_ageOfOnset" : f"P{record[1]}Y",
                                "measurement_date" : record[2],
                                "unit_concept_id" : record[3],
                                "value_source_value" : record[4]})
        dict_measures[person_id] = listValues
    return dict_measures


def get_individuals_exposures(listIds):
    dict_exposures = {}
    for person_id in listIds:
        records = individual_queries.sql_get_exposure(client, person_id=person_id)
        listValues = []
        for record in records:
            listValues.append({"observation_concept_id" : record[0],
                                "observation_ageOfOnset" : f"P{record[1]}Y",
                                "observation_date" : record[2]})
        dict_exposures[person_id] = listValues
    return dict_exposures 

def format_query(listIds, dictPerson, dictCondition, dictProcedures, dictMeasures, dictExposures):
    list_format = []
    for person_id in listIds:
        dictId = {"id":person_id}
        if any("gender_concept_id" in d for d in dictPerson[person_id]):
            dictId["sex"] = dictPerson[person_id][0]["gender_concept_id"]
        if any("race_concept_id" in d for d in dictPerson[person_id]):
            dictId["ethnicity"] = dictPerson[person_id][0]["race_concept_id"]
        if any("condition_concept_id" in d for d in dictCondition[person_id]):
            dictId["diseases"] = list(map(diseases_table_map, dictCondition[person_id]))
        if any("procedure_concept_id" in d for d in dictProcedures[person_id]):
            dictId["interventionsOrProcedures"] = list(map(procedures_table_map, dictProcedures[person_id]))
        if any("measurement_concept_id" in d for d in dictMeasures[person_id]):
            dictId["measures"] = list(map(measures_table_map, dictMeasures[person_id]))
        if any("observation_concept_id" in d for d in dictExposures[person_id]):
            dictId["exposures"] = list(map(exposures_table_map, dictExposures[person_id]))
        list_format.append(dictId)
    return list_format

def map_domains(domain_id):
    # Domain_id : Table in OMOP
    # Maybe there is more than one mapping in the condition domain
    dictMapping = {
        'Gender':{'person':'gender_concept_id'},
        'Race':{'person':'race_concept_id'},
        'Condition':{'condition_occurrence':'condition_concept_id'},
        'Measurement':{'measurement':'measurement_concept_id'},
        'Procedure':{'procedure_occurrence':'procedure_concept_id'},
        'Observation':{'observation':'observation_concept_id'},

    }
    return dictMapping[domain_id]

def search_descendants(concept_id):
    records = individual_queries.sql_get_descendants(client, concept_id=concept_id)

    l_descendants = set()
    for descendant in records:
        l_descendants.add(descendant[0])
    return l_descendants

def create_dynamic_filter(filters):
    base_filter = {
        'demografic_filters': '',
        'condition_filters': '',
        'measurement_filters': '',
        'procedures_filters': '',
        'exposures_filters': '',
    }

    list_person = []
    n_open_condition = 0
    query_condition = ""
    n_open_measurement = 0
    query_measurement = ""
    n_open_procedure = 0
    query_procedure = ""
    n_open_exposure = 0
    query_exposure = ""
    for filter in filters:
        # Default type of filter is ontology
        filterType = 'Ontology'
        if filter[2]:       # If filter has an operator (operator!=None) it is an Alphanumeric filter
            filterType = 'Alphanumeric'
        if "person" in filter[0]:
            variable_name = filter[0]['person']
            list_concept_id = []
            for concept_id in filter[1]:
                list_concept_id.append(variable_name + ' = ' + str(concept_id))
            query_person_id =  ' or '.join(list_concept_id)
            list_person.append(' ( ' + query_person_id + ' ) ')
        if "condition_occurrence" in filter[0]:
            n_open_condition += 1 
            variable_name = filter[0]['condition_occurrence']
            list_concept_id = []
            for concept_id in filter[1]:
                list_concept_id.append(variable_name + ' = ' + str(concept_id))
            query_person_id =  ' or '.join(list_concept_id)
            # This can be a function to no repeat always the same -> filter[0]
            query_condition += f"""
                and exists (
                    select 1
                    from cdm.condition_occurrence co
                    where p.person_id = co.person_id
                    and ({query_person_id})
            """
        if 'measurement' in filter[0]:
            n_open_measurement += 1 
            variable_name = filter[0]['measurement']
            list_concept_id = []
            for concept_id in filter[1]:
                if filterType == 'Alphanumeric':
                    value = filter[3]
                    list_concept_id.append(variable_name + ' = ' + str(concept_id) +
                                           ' and value_as_number ' + filter[2] + " " + value)
                else:
                    list_concept_id.append(variable_name + ' = ' + str(concept_id))
            query_person_id =  ' or '.join(list_concept_id)
            query_measurement += f"""
                and exists (
                    select 1
                    from cdm.measurement co
                    where p.person_id = co.person_id
                    and ({query_person_id})
            """
        if 'procedure_occurrence' in filter[0]:
            n_open_procedure += 1 
            variable_name = filter[0]['procedure_occurrence']
            list_concept_id = []
            for concept_id in filter[1]:
                list_concept_id.append(variable_name + ' = ' + str(concept_id))
            query_person_id =  ' or '.join(list_concept_id)
            query_procedure += f"""
                and exists (
                    select 1
                    from cdm.procedure_occurrence co
                    where p.person_id = co.person_id
                    and ({query_person_id})
            """
        if 'observation' in filter[0]:
            n_open_exposure += 1 
            variable_name = filter[0]['observation']
            list_concept_id = []
            for concept_id in filter[1]:
                list_concept_id.append(variable_name + ' = ' + str(concept_id))
            query_person_id =  ' or '.join(list_concept_id)
            query_exposure += f"""
                and exists (
                    select 1
                    from cdm.observation co
                    where p.person_id = co.person_id
                    and ({query_person_id})
            """
        
    query_condition += ')'* n_open_condition
    query_measurement += ')'* n_open_measurement
    query_procedure += ')'* n_open_procedure
    query_exposure += ')'* n_open_exposure

    if list_person:
        base_filter['demografic_filters'] += ' and ( ' + " and ".join(list_person) + ' ) '

    base_filter['condition_filters'] += query_condition
    base_filter['measurement_filters'] += query_measurement
    base_filter['procedures_filters'] += query_procedure
    base_filter['exposures_filters'] += query_exposure

    return base_filter

def super_query_count(filter):
    return  f""" select count(distinct person_id)
        from cdm.person p
        where true
        {filter['demografic_filters']}
        {filter['condition_filters']}
        {filter['measurement_filters']}
        {filter['procedures_filters']}
        {filter['exposures_filters']}

    """

def super_query_get(filter, offset, limit):
    return  f""" select person_id
        from cdm.person p
        where true
        {filter['demografic_filters']}
        {filter['condition_filters']}
        {filter['measurement_filters']}
        {filter['procedures_filters']}
        {filter['exposures_filters']}

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
        records = individual_queries.sql_get_concept_domain(client,
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
    print(query_get)
    records_get = basic_query(query_get)
    listOfList = [str(record[0]) for record in records_get]

    return listOfList, count_records[0][0]

# /individuals/?filters=SNOMED:0&filters=OMOP:23
def filters(filtersDict, offset, limit):
    if type(filtersDict[0]) is dict:         # If filter is from Post
        print(filtersDict)
        listFilters, count = checkFilters(filtersDict, offset, limit, 'POST')
    else:
        listFilters, count = checkFilters(filtersDict, offset, limit, 'GET')

    return listFilters, count
                                                      
def get_individuals(entry_id: Optional[str]=None, qparams: RequestParams=RequestParams()):

    schema = DefaultSchemas.INDIVIDUALS
    count_ids = 0

    if qparams.query.filters:
        listIds, count_ids = filters(qparams.query.filters,
                        offset=qparams.query.pagination.skip,
                        limit=qparams.query.pagination.limit)
        if count_ids == 0:
            return schema, count_ids, []
    else:
        listIds = get_individual_id(offset=qparams.query.pagination.skip,
                                            limit=qparams.query.pagination.limit,
                                            person_id=entry_id)                 # List with all Ids
        count_ids = individual_queries.count_individuals(client)   # Count individuals
        LOG.debug('Number of ids:' + str(count_ids))

    dictPerson = get_individuals_person(listIds)        # List with Id, sex, ethnicity
    dictCondition = get_individuals_condition(listIds)  # List with al the diseases per Id
    dictProcedures = get_individuals_procedure(listIds)
    dictMeasures = get_individuals_measures(listIds)
    dictExposures = get_individuals_exposures(listIds)

    dictPerson = search_ontologies(dictPerson)
    dictCondition = search_ontologies(dictCondition)
    dictProcedures = search_ontologies(dictProcedures)
    dictMeasures = search_ontologies(dictMeasures)
    dictExposures = search_ontologies(dictExposures)

    docs = format_query(listIds, dictPerson, dictCondition, dictProcedures, dictMeasures, dictExposures)
    LOG.debug(count_ids)
    return schema, count_ids, docs



def get_individual_with_id(entry_id: Optional[str], qparams: RequestParams):
    
    schema = DefaultSchemas.INDIVIDUALS

    if qparams.query.filters:
        originalListIds = filters(qparams.query.filters)
        if not entry_id in listIds:
            return schema, 0, []
    
    # Search Id
    listIds = get_individual_id(person_id=entry_id)

    dictPerson = get_individuals_person(listIds)
    dictCondition = get_individuals_condition(listIds)
    dictProcedures = get_individuals_procedure(listIds)
    dictMeasures = get_individuals_measures(listIds)
    dictExposures = get_individuals_exposures(listIds)


    dictPerson = search_ontologies(dictPerson)
    dictCondition = search_ontologies(dictCondition)
    dictProcedures = search_ontologies(dictProcedures)
    dictMeasures = search_ontologies(dictMeasures)
    dictExposures = search_ontologies(dictExposures)

    docs = format_query(listIds, dictPerson, dictCondition, dictProcedures, dictMeasures, dictExposures)

    return schema, 1, docs


# def get_individual_with_id(entry_id: Optional[str], qparams: RequestParams):
#     collection = 'individuals'
#     query = apply_request_parameters({}, qparams)
#     query = apply_filters(query, qparams.query.filters, collection)
#     query = query_id(query, entry_id)
#     query = include_resultset_responses(query, qparams)
#     schema = DefaultSchemas.INDIVIDUALS
#     count = get_count(client.beacon.individuals, query)
#     include = qparams.query.include_resultset_responses
#     if include == 'MISS':
#         pre_docs = get_documents(
#             client.beacon.individuals,
#             query,
#             qparams.query.pagination.skip,
#             count
#         )
#         negative_query={}
#         ids_array = []
#         for doc in pre_docs:
#             elem_query={}
#             elem_query['_id']=doc['_id']
#             ids_array.append(elem_query)
        
#         negative_query['$nor']=ids_array
#         LOG.debug(negative_query)
#         docs = get_documents(
#             client.beacon.individuals,
#             negative_query,
#             qparams.query.pagination.skip,
#             qparams.query.pagination.limit
#         )
#         count = get_count(client.beacon.individuals, negative_query)
#     else:
#         docs = get_documents(
#             client.beacon.individuals,
#             query,
#             qparams.query.pagination.skip,
#             qparams.query.pagination.limit
#         )
#     return schema, count, docs


def get_variants_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"$and": [{"id": entry_id}]}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    count = get_count(client.beacon.individuals, query)
    individual_ids = client.beacon.individuals \
        .find_one(query, {"id": 1, "_id": 0})
    LOG.debug(individual_ids)
    individual_ids=get_cross_query(individual_ids,'id','caseLevelData.biosampleId')
    LOG.debug(individual_ids)
    query = apply_filters(individual_ids, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.GENOMICVARIATIONS
    count = get_count(client.beacon.genomicVariations, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.genomicVariations,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.genomicVariations,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.genomicVariations, negative_query)
    else:
        docs = get_documents(
            client.beacon.genomicVariations,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs


def get_biosamples_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.BIOSAMPLES
    count = get_count(client.beacon.biosamples, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.biosamples,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.biosamples,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.biosamples, negative_query)
    else:
        docs = get_documents(
            client.beacon.biosamples,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs


def get_filtering_terms_of_individual(entry_id: Optional[str], qparams: RequestParams):
    schema = DefaultSchemas.FILTERINGTERMS

    l_sql_filters = [individual_queries.sql_filtering_terms_race_gender(client),
                    individual_queries.sql_filtering_terms_condition(client),
                    individual_queries.sql_filtering_terms_measurement(client),
                    individual_queries.sql_filtering_terms_procedure(client),
                    individual_queries.sql_filtering_terms_observation(client)]
    l_indFilters = []
    for ind_filters in l_sql_filters:
        for filters in ind_filters:
            if filters[0].endswith("OMOP generated"):
                continue
            dict_filter = {"id":filters[0],"label":filters[1],"scopes":["individual"],"type":"ontology"}
            l_indFilters.append(dict_filter)
    return schema, len(l_indFilters), l_indFilters



def get_runs_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.RUNS
    count = get_count(client.beacon.runs, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.runs,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.runs,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.runs, negative_query)
    else:
        docs = get_documents(
            client.beacon.runs,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs

def get_analyses_of_individual(entry_id: Optional[str], qparams: RequestParams):
    collection = 'individuals'
    query = {"individualId": entry_id}
    query = apply_request_parameters(query, qparams)
    query = apply_filters(query, qparams.query.filters, collection)
    query = include_resultset_responses(query, qparams)
    schema = DefaultSchemas.ANALYSES
    count = get_count(client.beacon.analyses, query)
    include = qparams.query.include_resultset_responses
    if include == 'MISS':
        pre_docs = get_documents(
            client.beacon.analyses,
            query,
            qparams.query.pagination.skip,
            count
        )
        negative_query={}
        ids_array = []
        for doc in pre_docs:
            elem_query={}
            elem_query['_id']=doc['_id']
            ids_array.append(elem_query)
        
        negative_query['$nor']=ids_array
        LOG.debug(negative_query)
        docs = get_documents(
            client.beacon.analyses,
            negative_query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
        count = get_count(client.beacon.analyses, negative_query)
    else:
        docs = get_documents(
            client.beacon.analyses,
            query,
            qparams.query.pagination.skip,
            qparams.query.pagination.limit
        )
    return schema, count, docs
