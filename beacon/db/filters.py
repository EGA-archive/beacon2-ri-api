import collections
from typing import List, Union
import re
import json
from copy import deepcopy

from beacon.request import ontologies
from beacon.request.model import AlphanumericFilter, CustomFilter, OntologyFilter, Operator, Similarity
from beacon.db.utils import get_documents, join_query
from beacon.db import client

import logging

LOG = logging.getLogger(__name__)

CURIE_REGEX = r'^([a-zA-Z0-9]*):\/?[a-zA-Z0-9]*$'

def apply_filters(query: dict, filters: List[dict], collection: str, query_parameters: dict) -> dict:
    LOG.debug(query)
    #LOG.debug("Filters len = {}".format(len(filters)))
    request_parameters = query_parameters
    LOG.debug(request_parameters)
    total_query={}
    if len(filters) >= 1:
        total_query["$and"] = []
        if query != {} and request_parameters == {}:
            total_query["$and"].append(query)
        for filter in filters:
            partial_query = {}
            if "value" in filter:
                #LOG.debug(filter)
                filter = AlphanumericFilter(**filter)
                LOG.debug("Alphanumeric filter: %s %s %s", filter.id, filter.operator, filter.value)
                partial_query = apply_alphanumeric_filter(partial_query, filter, collection)
            elif "includeDescendantTerms" not in filter and '.' not in filter["id"] and filter["id"].isupper():
                filter=OntologyFilter(**filter)
                filter.include_descendant_terms=True
                #LOG.debug("Ontology filter: %s", filter.id)
                #partial_query = {"$text": defaultdict(str) }
                #partial_query =  { "$text": { "$search": "" } } 
                partial_query = apply_ontology_filter(partial_query, filter, collection, request_parameters)
            elif "similarity" in filter or "includeDescendantTerms" in filter or re.match(CURIE_REGEX, filter["id"]) and filter["id"].isupper():
                filter = OntologyFilter(**filter)
                LOG.debug("Ontology filter: %s", filter.id)
                #partial_query = {"$text": defaultdict(str) }
                #partial_query =  { "$text": { "$search": "" } } 
                #LOG.debug(partial_query)
                partial_query = apply_ontology_filter(partial_query, filter, collection)
            else:
                filter = CustomFilter(**filter)
                LOG.debug("Custom filter: %s", filter.id)
                partial_query = apply_custom_filter(partial_query, filter, collection)
            #LOG.debug(partial_query)
            total_query["$and"].append(partial_query)
            #LOG.debug(query)
            if total_query["$and"] == [{'$or': []}] or total_query['$and'] == []:
                total_query = {}
    elif request_parameters != {}:
        LOG.debug('holaaaaaa')
        try:
            if len(request_parameters["$or"]) > 1:
                LOG.debug('holaaaa')
                array_of_biosamples2=[]
                array_of_biosamples=[]
                for reqpam in request_parameters["$or"]:
                    biosample_ids = client.beacon.genomicVariations.find(reqpam, {"caseLevelData.biosampleId": 1, "_id": 0})
                    for biosample in biosample_ids:
                        for bioitem in biosample['caseLevelData']:
                            if bioitem not in array_of_biosamples2:
                                array_of_biosamples2.append(bioitem["biosampleId"])
                        array_of_biosamples.append(array_of_biosamples2)
                        array_of_biosamples2=[]
                
                dict_counts={}
                for list_bio in array_of_biosamples:
                    for item in list_bio:
                        if item not in array_of_biosamples2:
                            array_of_biosamples2.append(item)
                        try:
                            dict_counts[item]+=1
                        except Exception:
                            dict_counts[item]=1
                partial_query={}
                partial_query['$or']=[]
                for item in array_of_biosamples2:
                    if dict_counts[item] == len(request_parameters["$or"]):
                        partial_query['$or'].append({"id": item})

                mongo_collection=client.beacon.biosamples
                original_id="individualId"
                join_ids2=list(join_query(mongo_collection, partial_query, original_id))
                def_list=[]
                final_id="id"
                for id_item in join_ids2:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                partial_query={}
                partial_query['$or']=def_list
                total_query["$and"]=[]
                total_query["$and"].append(partial_query)
        except Exception:
            partial_query = {}
            LOG.debug(request_parameters)
            biosample_ids = client.beacon.genomicVariations.find(request_parameters, {"caseLevelData.biosampleId": 1, "_id": 0})
            LOG.debug(biosample_ids)
            final_id='id'
            original_id="biosampleId"
            def_list=[]
            partial_query['$or']=[]
            for iditem in biosample_ids:
                for id_item in iditem['caseLevelData']:
                    if isinstance(id_item, dict):
                        new_id={}
                        new_id[final_id] = id_item[original_id]
                        try:
                            partial_query['$or'].append(new_id)
                        except Exception:
                            def_list.append(new_id)
            LOG.debug(partial_query)
            
            mongo_collection=client.beacon.biosamples
            original_id="individualId"
            join_ids2=list(join_query(mongo_collection, partial_query, original_id))
            def_list=[]
            final_id="id"
            for id_item in join_ids2:
                new_id={}
                new_id[final_id] = id_item.pop(original_id)
                def_list.append(new_id)
            partial_query={}
            partial_query['$or']=def_list
            if def_list != []:
                try:
                    partial_query['$or'].def_list
                except Exception:
                    partial_query={}
                    partial_query['$or']=def_list
            total_query["$and"]=[]
            total_query["$and"].append(partial_query)
            #LOG.debug(query)
            if total_query["$and"] == [{'$or': []}] or total_query['$and'] == []:
                total_query = {}
    else:
        total_query=query

    LOG.debug(total_query)
    return total_query


def apply_ontology_filter(query: dict, filter: OntologyFilter, collection: str, request_parameters: dict) -> dict:
    scope = filter.scope
    is_filter_id_required = True
    # Search similar
    if filter.similarity != Similarity.EXACT:
        is_filter_id_required = False
        ontology_list=filter.id.split(':')
        if filter.similarity == Similarity.HIGH:
            similarity_high=[]
            ontology_dict=client.beacon.similarities.find({"id": filter.id})
            final_term_list = ontology_dict[0]["similarity_high"]
        elif filter.similarity == Similarity.MEDIUM:
            similarity_medium=[]
            ontology_dict=client.beacon.similarities.find({"id": filter.id})
            final_term_list = ontology_dict[0]["similarity_medium"]
        elif filter.similarity == Similarity.LOW:
            similarity_low=[]
            ontology_dict=client.beacon.similarities.find({"id": filter.id})
            final_term_list = ontology_dict[0]["similarity_low"]
        
        final_term_list.append(filter.id)
        query_filtering={}
        query_filtering['$and']=[]
        dict_scope['scope']=scope
        query_filtering['$and'].append(dict_scope)
        dict_id={}
        dict_id['id']=filter.id
        query_filtering['$and'].append(dict_id)
        docs = get_documents(
            client.beacon.filtering_terms,
            query_filtering,
            0,
            1
        )
            
        for doc_term in docs:
            LOG.debug(doc_term)
            label = doc_term['label']
        if scope == 'genomicVariations' and collection == 'g_variants' or scope == collection:
            query_filtering={}
            query_filtering['$and']=[]
            query_filtering['$and'].append(dict_scope)
            dict_regex={}
            try:
                dict_regex['$regex']=label
            except Exception:
                dict_regex['$regex']=''
            dict_id={}
            dict_id['id']=dict_regex
            query_filtering['$and'].append(dict_id)
            docs_2 = get_documents(
                client.beacon.filtering_terms,
                query_filtering,
                0,
                1
            )
            for doc2 in docs_2:
                query_terms = doc2['id']
            query_terms = query_terms.split(':')
            query_term = query_terms[0] + '.id'
            query_id={}
            query['$or']=[]
            for simil in final_term_list:
                query_id={}
                query_id[query_term]=simil
                query['$or'].append(query_id)
            LOG.debug(query)
        else:
            pass
        

    # Apply descendant terms
    if filter.include_descendant_terms == True:
        final_term_list=[]
        final_term_list.append(filter.id)
        is_filter_id_required = False
        ontology=filter.id.replace("\n","")
        #LOG.debug(ontology)
        list_descendant = []
        try:
            ontology_dict=client.beacon.similarities.find({"id": ontology})
            list_descendant = ontology_dict[0]["descendants"]
        except Exception:
            pass

        try: 
            if query['$or']:
                pass
            else:
                query['$or']=[]
        except Exception:
            query['$or']=[]
        list_descendant.append(filter.id)
        query_filtering={}
        query_filtering['$and']=[]
        dict_scope={}

        dict_scope['scope']=scope
        dict_id={}
        dict_id['id']=filter.id
        query_filtering['$and'].append(dict_id)
        query_filtering['$and'].append(dict_scope)
        LOG.debug(query_filtering)
        docs = get_documents(
            client.beacon.filtering_terms,
            query_filtering,
            0,
            1
        )

        for doc_term in docs:
            LOG.debug(doc_term)
            label = doc_term['label']
        query_filtering={}
        query_filtering['$and']=[]
        dict_regex={}
        try:
            dict_regex['$regex']=label
        except Exception:
            dict_regex['$regex']=''
        dict_id={}
        dict_id['id']=dict_regex
        dict_scope={}
        dict_scope['scope']=scope
        query_filtering['$and'].append(dict_id)
        query_filtering['$and'].append(dict_scope)
        docs_2 = get_documents(
            client.beacon.filtering_terms,
            query_filtering,
            0,
            1
        )
        for doc2 in docs_2:
            query_terms = doc2['id']
            query_terms = query_terms.split(':')
            query_term = query_terms[0] + '.id'

        query_id={}
        query['$or']=[]
        for simil in final_term_list:
            query_id={}
            query_id[query_term]=simil
            query['$or'].append(query_id)
        
        LOG.debug(query)

        if scope == 'genomicVariations' and collection == 'g_variants' or scope == collection:
            LOG.debug(query)
            LOG.debug(request_parameters)
            subquery={}
            subquery["$or"]=[]
            if request_parameters != {}:
                biosample_ids = client.beacon.genomicVariations.find(request_parameters, {"caseLevelData.biosampleId": 1, "_id": 0})
                final_id='id'
                original_id="biosampleId"
                def_list=[]
                for iditem in biosample_ids:
                    for id_item in iditem['caseLevelData']:
                        if isinstance(id_item, dict):
                            new_id={}
                            new_id[final_id] = id_item[original_id]
                            try:
                                subquery['$or'].append(new_id)
                            except Exception:
                                def_list.append(new_id)
                
                LOG.debug(subquery)
                mongo_collection=client.beacon.biosamples
                original_id="individualId"
                join_ids2=list(join_query(mongo_collection, subquery, original_id))
                def_list=[]
                final_id="id"
                for id_item in join_ids2:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                subquery={}
                subquery['$or']=def_list
                try:
                    LOG.debug(query)
                    query["$and"] = []
                    query["$and"].append(subquery)
                except Exception:
                    LOG.debug(query)
            LOG.debug(query)
        else:
            def_list=[]
            if scope == 'individuals' and collection == 'g_variants':
                mongo_collection=client.beacon.individuals
                original_id="id"
                join_ids=list(join_query(mongo_collection, query, original_id))
                final_id="individualId"
                for id_item in join_ids:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                query={}
                query['$or']=def_list
                mongo_collection=client.beacon.biosamples
                original_id="id"
                join_ids2=list(join_query(mongo_collection, query, original_id))
                def_list=[]
                final_id="caseLevelData.biosampleId"
                for id_item in join_ids2:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                query={}
                query['$or']=def_list
            elif scope == 'genomicVariations' and collection == 'individuals':
                biosample_ids = client.beacon.genomicVariations.find(query, {"caseLevelData.biosampleId": 1, "_id": 0})
                final_id='id'
                original_id="biosampleId"
                def_list=[]
                for iditem in biosample_ids:
                    for id_item in iditem['caseLevelData']:
                        if isinstance(id_item, dict):
                            new_id={}
                            new_id[final_id] = id_item[original_id]
                            try:
                                #LOG.debug(new_id)
                                query['$or'].append(new_id)
                            except Exception:
                                def_list.append(new_id)
                if def_list != []:
                    try:
                        query['$or'].def_list
                    except Exception:
                        query={}
                        query['$or']=def_list
                mongo_collection=client.beacon.biosamples
                original_id="individualId"
                join_ids2=list(join_query(mongo_collection, query, original_id))
                def_list=[]
                final_id="id"
                for id_item in join_ids2:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                query={}
                query['$or']=def_list
                if def_list != []:
                    try:
                        query['$or'].def_list
                    except Exception:
                        query={}
                        query['$or']=def_list
            elif scope == 'runs' and collection == 'g_variants':
                mongo_collection=client.beacon.runs
                original_id="biosampleId"
                join_ids=list(join_query(mongo_collection, query, original_id))
                final_id="caseLevelData.biosampleId"
                for id_item in join_ids:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                query={}
                query['$or']=def_list
            elif scope == 'runs' and collection == 'individuals':
                LOG.debug(query)
                mongo_collection=client.beacon.runs
                original_id="individualId"
                join_ids=list(join_query(mongo_collection, query, original_id))
                final_id="id"
                for id_item in join_ids:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                query={}
                query['$or']=def_list
            elif scope == 'individuals' and collection == 'runs':
                mongo_collection=client.beacon.individuals
                original_id="id"
                join_ids=list(join_query(mongo_collection, query, original_id))
                final_id="individualId"
                for id_item in join_ids:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                query={}
                query['$or']=def_list
            
    if is_filter_id_required:
        query_filtering={}
        query_filtering['$and']=[]
        dict_scope={}
        dict_scope['scope']=scope
        query_filtering['$and'].append(dict_scope)
        dict_id={}
        dict_id['id']=filter.id
        query_filtering['$and'].append(dict_id)
        docs = get_documents(
        client.beacon.filtering_terms,
        query_filtering,
        0,
        1
    )
        
        for doc_term in docs:
            LOG.debug(doc_term)
            label = doc_term['label']
        query_filtering={}
        query_filtering['$and']=[]
        query_filtering['$and'].append(dict_scope)
        dict_regex={}
        dict_regex['$regex']=label
        dict_id={}
        dict_id['id']=dict_regex
        query_filtering['$and'].append(dict_id)
        docs_2 = get_documents(
        client.beacon.filtering_terms,
        query_filtering,
        0,
        1
    )
        for doc2 in docs_2:
            query_terms = doc2['id']
        query_terms = query_terms.split(':')
        query_term = query_terms[0] + '.id'
        query[query_term]=filter.id
        LOG.debug(query)
   

    #LOG.debug("QUERY: %s", query)
    return query

def format_value(value: Union[str, List[int]]) -> Union[List[int], str, int, float]:
    if isinstance(value, list):
        return value
    
    elif value.isnumeric():
        if float(value).is_integer():
            return int(value)
        else:
            return float(value)
    
    else:
        return value

def format_operator(operator: Operator) -> str:
    if operator == Operator.EQUAL:
        return "$eq"
    elif operator == Operator.NOT:
        return "$ne"
    elif operator == Operator.GREATER:
        return "$gt"
    elif operator == Operator.GREATER_EQUAL:
        return "$gte"
    elif operator == Operator.LESS:
        return "$lt"
    else:
        # operator == Operator.LESS_EQUAL
        return "$lte"

def apply_alphanumeric_filter(query: dict, filter: AlphanumericFilter, collection: str) -> dict:
    #LOG.debug(filter.value)
    scope = filter.scope
    formatted_value = format_value(filter.value)
    formatted_operator = format_operator(filter.operator)
    #LOG.debug(collection)
    #LOG.debug(filter.id)
    if collection == 'g_variants' and scope != 'individuals' and scope != 'runs':
        if filter.id == "identifiers.genomicHGVSId":
            list_chromosomes = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22']
            dict_regex={}
            if filter.value == 'GRCh38':
                dict_regex['$regex']="11:"
            elif filter.value == 'GRCh37':
                dict_regex['$regex']="10:"
            elif filter.value == 'NCBI36':
                dict_regex['$regex']="9:"
            elif filter.value in list_chromosomes:
                dict_regex['$regex']='^NC_0000'+filter.value
            elif '>' in filter.value:
                dict_regex=filter.value
            elif '.' in filter.value:
                valuesplitted = filter.value.split('.')
                dict_regex['$regex']=valuesplitted[0]+".*"+valuesplitted[-1]+":"
                dict_regex['$options']= "si"
            query[filter.id] = dict_regex
        elif filter.id == 'molecularAttributes.aminoacidChanges':
            query[filter.id] = filter.value
        elif filter.id == 'molecularAttributes.geneIds':
            LOG.debug('holaaaa')
            query[filter.id] = filter.value
        elif filter.id == "caseLevelData.clinicalInterpretations.clinicalRelevance":
            query[filter.id] = filter.value
        elif filter.id == "variantInternalId":
            if 'max' in filter.value:
                valuereplaced = filter.value.replace('max', '')
                length=40+int(valuereplaced)+1
                array_min=[]
                dict_len={}
                dict_len['$strLenCP']="$variantInternalId"
                array_min.append(dict_len)
                array_min.append(length)
                dict_gt={}
                dict_gt['$lt']=array_min
                dict_expr={}
                dict_expr['$expr']=dict_gt

                            
                query=dict_expr

            elif 'min' in filter.value:
                valuereplaced = filter.value.replace('min', '')
                length=40+int(valuereplaced)-1
                array_min=[]
                dict_len={}
                dict_len['$strLenCP']="$variantInternalId"
                array_min.append(dict_len)
                array_min.append(length)
                dict_gt={}
                dict_gt['$gt']=array_min
                dict_expr={}
                dict_expr['$expr']=dict_gt

                            
                query=dict_expr





        else:
            formatted_value = format_value(filter.value)
            formatted_operator = format_operator(filter.operator)
            query[filter.id] = { formatted_operator: formatted_value }
    elif isinstance(formatted_value,str):
        if formatted_operator == "$eq":
            if '%' in filter.value:
                try: 
                    if query['$or']:
                        pass
                    else:
                        query['$or']=[]
                except Exception:
                    query['$or']=[]
                value_splitted=filter.value.split('%')
                regex_dict={}
                regex_dict['$regex']=value_splitted[1]
                if filter.id == 'libraryStrategy':
                    query_term = filter.id
                else:
                    query_term = filter.id + '.' + 'label'
                query_id={}
                query_id[query_term]=regex_dict
                query['$or'].append(query_id)
                

            else:
                try: 
                    if query['$or']:
                        pass
                    else:
                        query['$or']=[]
                except Exception:
                    query['$or']=[]
                query_term = filter.id + '.' + 'label'
                query_id={}
                query_id[query_term]=filter.value
                query['$or'].append(query_id) 
            LOG.debug(collection)
            LOG.debug(scope)
            if scope == 'runs' and collection == 'individuals':
                #LOG.debug(query)
                mongo_collection=client.beacon.runs
                original_id="individualId"
                join_ids=list(join_query(mongo_collection, query, original_id))
                final_id="id"
                def_list=[]
                for id_item in join_ids:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                query={}
                query['$or']=def_list
            elif scope == 'runs' and collection == 'g_variants':
                LOG.debug(query)
                mongo_collection=client.beacon.runs
                original_id="biosampleId"
                join_ids=list(join_query(mongo_collection, query, original_id))
                final_id="caseLevelData.biosampleId"
                def_list=[]
                for id_item in join_ids:
                    new_id={}
                    new_id[final_id] = id_item.pop(original_id)
                    def_list.append(new_id)
                query={}
                query['$or']=def_list
        elif formatted_operator == "$ne":
            if '%' in filter.value:
                try: 
                    if query['$nor']:
                        pass
                    else:
                        query['$nor']=[]
                except Exception:
                    query['$nor']=[]
                value_splitted=filter.value.split('%')
                regex_dict={}
                regex_dict['$regex']=value_splitted[1]
                query_term = filter.id + '.' + 'label'
                query_id={}
                query_id[query_term]=regex_dict
                query['$nor'].append(query_id)
            else:
                try: 
                    if query['$nor']:
                        pass
                    else:
                        query['$nor']=[]
                except Exception:
                    query['$nor']=[]

                query_term = filter.id + '.' + 'label'
                query_id={}
                query_id[query_term]=filter.value
                query['$nor'].append(query_id) 
    else:
        query['measurementValue.value'] = { formatted_operator: float(formatted_value) }
        if "LOINC" in filter.id:
            query['assayCode.id']=filter.id
        else:
            query['assayCode.label']=filter.id
        #LOG.debug(query)
        dict_elemmatch={}
        dict_elemmatch['$elemMatch']=query
        dict_measures={}
        dict_measures['measures']=dict_elemmatch
        query = dict_measures
        def_list=[]
        LOG.debug(collection)
        if collection == 'g_variants':
            mongo_collection=client.beacon.individuals
            original_id="id"
            join_ids=list(join_query(mongo_collection, query, original_id))
            final_id="individualId"
            for id_item in join_ids:
                new_id={}
                new_id[final_id] = id_item.pop(original_id)
                def_list.append(new_id)
            query={}
            query['$or']=def_list
            mongo_collection=client.beacon.biosamples
            original_id="id"
            join_ids2=list(join_query(mongo_collection, query, original_id))
            def_list=[]
            final_id="caseLevelData.biosampleId"
            for id_item in join_ids2:
                new_id={}
                new_id[final_id] = id_item.pop(original_id)
                def_list.append(new_id)
            query={}
            query['$or']=def_list
            LOG.debug(query)

    #LOG.debug("QUERY: %s", query)
    return query



def apply_custom_filter(query: dict, filter: CustomFilter, collection:str) -> dict:
    #LOG.debug(query)

    value_splitted = filter.id.split(':')
    query_term = value_splitted[0] + '.label'
    query[query_term]=value_splitted[1]


    #LOG.debug("QUERY: %s", query)
    return query
