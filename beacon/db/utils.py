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

def get_total_count(collection: Collection, query: dict) -> int:
    #LOG.debug("Returning estimated count")
    return collection.estimated_document_count()

def get_count(collection: Collection, query: dict) -> int:
    if not query:
        #LOG.debug("Returning estimated count")
        return collection.estimated_document_count()
    else:
        counts=client.beacon.counts.find({"id": str(query), "collection": str(collection)})
        try:
            counts=list(counts)
            if counts == []:
                match_dict={}
                match_dict['$match']=query
                count_dict={}
                aggregated_query=[]
                count_dict["$count"]='Total'
                aggregated_query.append(match_dict)
                aggregated_query.append(count_dict)
                total=list(collection.aggregate(aggregated_query))
                insert_dict={}
                insert_dict['id']=str(query)
                total_counts=total[0]['Total']
                insert_dict['num_results']=total_counts
                insert_dict['collection']=str(collection)
                insert_total=client.beacon.counts.insert_one(insert_dict)
            else:
                total_counts=counts[0]["num_results"]
        except Exception:
            try:
                total_counts=client.beacon.counts.count_documents(query)
                insert_dict={}
                insert_dict['id']=str(query)
                insert_dict['num_results']=total_counts
                insert_dict['collection']=str(collection)
                insert_total=client.beacon.counts.insert_one(insert_dict)
            except Exception:
                total_counts=15
        return total_counts

def get_documents(collection: Collection, query: dict, skip: int, limit: int) -> Cursor:
    LOG.debug("FINAL QUERY: {}".format(query))
    ##LOG.debug(skip)
    return collection.find(query).skip(skip).limit(limit).max_time_ms(100 * 1000)

def get_aggregated_documents(collection: Collection, query: dict) -> Cursor:
    ##LOG.debug("FINAL QUERY: {}".format(query))
    return list(collection.aggregate(query))

def get_filtering_documents(collection: Collection, query: dict, remove_id: dict,skip: int, limit: int) -> Cursor:
    ##LOG.debug("FINAL QUERY: {}".format(query))
    return collection.find(query,remove_id).skip(skip).limit(limit).max_time_ms(100 * 1000)

def get_cross_query(ids: dict, cross_type: str, collection_id: str):
    id_list=[]
    dict_in={}
    id_dict={}
    if cross_type == 'biosampleId' or cross_type=='id':
        list_item=ids
        #LOG.debug(str(list_item))
        id_list.append(str(list_item))
        dict_in["$in"]=id_list
        #LOG.debug(id_list)
        id_dict[collection_id]=dict_in
        query = id_dict
    elif cross_type == 'individualIds' or cross_type=='biosampleIds':
        list_individualIds=ids
        dict_in["$in"]=list_individualIds
        #LOG.debug(list_individualIds)
        id_dict[collection_id]=dict_in
        query = id_dict
    else:
        for k, v in ids.items():
            for item in v:
                id_list.append(item[cross_type])
        dict_in["$in"]=id_list
        id_dict[collection_id]=dict_in
        query = id_dict


    #LOG.debug(query)
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


    #LOG.debug(query)
    return query

def join_query(collection: Collection,query: dict, original_id):
    #LOG.debug(query)
    excluding_fields={"_id": 0, original_id: 1}
    return collection.find(query, excluding_fields).max_time_ms(100 * 1000)

def id_to_biosampleId(collection: Collection,query: dict, original_id):
    #LOG.debug(query)
    excluding_fields={"_id": 0, original_id: 1}
    return collection.find(query, excluding_fields).max_time_ms(100 * 1000)

def get_docs_by_response_type(include: str, query: dict, datasets_dict: dict, dataset: str, limit: int, skip: int, mongo_collection, idq: str):
    if include == 'MISS':
        count = 0
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
                    #LOG.debug(dataset_count)
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
        count=0
        #LOG.debug(query)
        #LOG.debug(count)
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
                    #LOG.debug(query_count)
                    dataset_count = get_count(mongo_collection, query)
                    #LOG.debug(dataset_count)
                    #LOG.debug(limit)
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
        count=0
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
                    #LOG.debug(dataset_count)
                    docs = get_documents(
                        mongo_collection,
                        query_count,
                        skip*limit,
                        limit
                    )
                else:
                    dataset_count=0
    return count, dataset_count, docs
