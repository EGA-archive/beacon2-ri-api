from typing import Dict, Optional

import imp

from pymongo.cursor import Cursor
from pymongo.collection import Collection

file, pathname, description = imp.find_module('beacon', [''])
my_module = imp.load_module('beacon', file, pathname, description)

from beacon.request import RequestParams

from beacon.db import client


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
        #LOG.debug("FINAL QUERY (COUNT): {}".format(query))
        LOG.debug("Returning count")
        return collection.count_documents(query)


def get_documents(collection: Collection, query: dict, skip: int, limit: int) -> Cursor:
    #LOG.debug("FINAL QUERY: {}".format(query))
    LOG.debug(skip)
    return collection.find(query).skip(skip).limit(limit).max_time_ms(10 * 1000)

def get_aggregated_documents(collection: Collection, query: dict) -> Cursor:
    #LOG.debug("FINAL QUERY: {}".format(query))
    return list(collection.aggregate(query))

def get_filtering_documents(collection: Collection, query: dict, remove_id: dict,skip: int, limit: int) -> Cursor:
    #LOG.debug("FINAL QUERY: {}".format(query))
    return collection.find(query,remove_id).skip(skip).limit(limit).max_time_ms(10 * 1000)

def get_cross_query(ids: dict, cross_type: str, collection_id: str):
    id_list=[]
    dict_in={}
    id_dict={}
    if cross_type == 'biosampleId' or cross_type=='id':
        list_item=ids
        LOG.debug(str(list_item))
        id_list.append(str(list_item))
        dict_in["$in"]=id_list
        LOG.debug(id_list)
        id_dict[collection_id]=dict_in
        query = id_dict
    elif cross_type == 'individualIds' or cross_type=='biosampleIds':
        list_individualIds=ids
        dict_in["$in"]=list_individualIds
        LOG.debug(list_individualIds)
        id_dict[collection_id]=dict_in
        query = id_dict
    else:
        for k, v in ids.items():
            for item in v:
                id_list.append(item[cross_type])
        dict_in["$in"]=id_list
        id_dict[collection_id]=dict_in
        query = id_dict


    LOG.debug(query)
    return query

def get_cross_query_variants(ids: dict, cross_type: str, collection_id: str):
    id_list=[]
    dict_in={}
    id_dict={}
    for k, v in ids.items():
        for item in v:
            id_list.append(item[cross_type])
    dict_in["$in"]=id_list
    id_dict[collection_id]=dict_in
    query = id_dict


    LOG.debug(query)
    return query

def join_query(aggregation_list: list, filter_id_list: list, match_big: dict, qparams: RequestParams, idq: str, datasets_dict: dict, dataset: str, mongo_collection):
    query_count={}
    i=1
    query_count["$or"]=[]
    for k, v in datasets_dict.items():
        LOG.debug(dataset)
        
        if k == dataset:
            LOG.debug(v)
            for id in v:
                if i <= len(v):
                    queryid={}
                    queryid[idq]=id
                    query_count["$or"].append(queryid)
                    i+=1
                else:
                    queryid={}
                    queryid[idq]=id
                    query_count["$or"].append(queryid)
                    i=1
    LOG.debug(query_count)
    match_or={}
    limit = qparams.query.pagination.limit

    
    j=0
    aggregated_query=[]
    count_query=[]
    lookup={}
    lookup['from']=aggregation_list[0]["scope"]
    lookup['localField']=idq
    if aggregation_list[0]["scope"] == 'g_variants':
        lookup['foreignField']="caseLevelData.biosampleId"
    elif aggregation_list[0]["scope"] == 'analyses':
        lookup['foreignField']="biosampleId"
    elif aggregation_list[0]["scope"] == 'runs':
        lookup['foreignField']="biosampleId"
    else:
        lookup['foreignField']="id"
    lookup['as']="aggregation"
    lookup_big={}
    lookup_big["$lookup"]=lookup
    aggregated_query.append(lookup_big)
    count_query.append(lookup_big)
    unwind={}
    unwind['path']="$aggregation"
    unwind['preserveNullAndEmptyArrays']=False
    unwind_big={}
    unwind_big["$unwind"]=unwind
    aggregated_query.append(unwind_big)
    count_query.append(unwind_big)
    if match_big != {}:
        aggregated_query.append(match_big)
        count_query.append(match_big)
    j=0
    k=0
    match2_big={}
    new_query={}
    new_query['$or']=[]
    for item in aggregation_list:
        for element in item["aggregate"][0]['$or']:
            new_dict={}
            for k,v in element.items():
                newkey='aggregation.'+k
                new_dict[newkey]=v
                new_query['$or'].append(new_dict)

    match2_big["$match"]=new_query
    aggregated_query.append(match2_big)
    if query_count["$or"]!=[]:
        match_or["$match"]=query_count
        aggregated_query.append(match_or)
        count_query.append(match_or)
    project={}
    project['aggregation']=0
    project_big={}
    project_big["$project"]=project
    aggregated_query.append(project_big)
    count_query.append(project_big)
    skip_dict={}
    skip_dict["$skip"]=qparams.query.pagination.skip*limit
    aggregated_query.append(skip_dict)
    limit_dict={}
    if limit == 0 or limit > 100:
        limit_dict["$limit"]=100
    else:
        limit_dict["$limit"]=limit
    aggregated_query.append(limit_dict)
    count = 0
    LOG.debug(aggregated_query)
    docs = get_aggregated_documents(
    mongo_collection,
    aggregated_query)
    count_dict={}
    count_dict["$count"]='Total'
    aggregated_query.append(count_dict)
    dataset_count=get_aggregated_documents(mongo_collection, aggregated_query)
    #dataset_count=client.beacon.genomicVariations.count_documents(aggregated_query)
    try:
        dataset_count=dataset_count[0]['Total']
    except Exception:
        dataset_count=0
    LOG.debug(dataset_count)
    return count, dataset_count, docs

def get_docs_by_response_type(include: str, query: dict, datasets_dict: dict, dataset: str, limit: int, skip: int, mongo_collection, idq: str):
    if include == 'MISS':
        count = get_count(mongo_collection, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid[idq]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid[idq]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(mongo_collection, query_count)
                    if limit == 0 or dataset_count < limit:
                        pass
                    else:
                        dataset_count = limit
                    if dataset_count !=0:
                        return count, -1, None
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        mongo_collection,
                        query_count,
                        skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    elif include == 'NONE':
        count = get_count(mongo_collection, query)
        dataset_count=0
        docs = get_documents(
        mongo_collection,
        query,
        skip*limit,
        limit
        )
    elif include == 'HIT':
        LOG.debug(query)
        count = get_count(mongo_collection, query)
        LOG.debug(count)
        query_count=query
        i=1
        query_count["$or"]=[]
        for k, v in datasets_dict.items():
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid[idq]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid[idq]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(mongo_collection, query_count)
                    LOG.debug(dataset_count)
                    LOG.debug(limit)
                    docs = get_documents(
                        mongo_collection,
                        query_count,
                        skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
        if dataset_count==0:
            return count, -1, None
    elif include == 'ALL':
        count = get_count(mongo_collection, query)
        query_count=query
        i=1
        for k, v in datasets_dict.items():
            query_count["$or"]=[]
            if k == dataset:
                for id in v:
                    if i < len(v):
                        queryid={}
                        queryid[idq]=id
                        query_count["$or"].append(queryid)
                        i+=1
                    else:
                        queryid={}
                        queryid[idq]=id
                        query_count["$or"].append(queryid)
                        i=1
                if query_count["$or"]!=[]:
                    dataset_count = get_count(mongo_collection, query_count)
                    if limit == 0 or dataset_count < limit:
                        pass
                    else:
                        dataset_count = limit
                    LOG.debug(dataset_count)
                    docs = get_documents(
                        mongo_collection,
                        query_count,
                        skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    return count, dataset_count, docs
