import logging

from aiohttp.web import json_response

from ..utils.exceptions import BeaconBadRequest
from ..validation.request import RequestParameters, print_qparams
from ..validation.fields import (RegexField,
                                 ChoiceField,
                                 IntegerField,
                                 ListField,
                                 DatasetsField)

LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                         QUERY VALIDATION
# ----------------------------------------------------------------------------------------------------------------------

class QueryParameters(RequestParameters):
    referenceName = ChoiceField("1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14",
                                "15", "16", "17", "18", "19", "20",
                                "21", "22", "X", "Y", "MT", required=True)
    start = IntegerField(min_value=0)
    end = IntegerField(min_value=0)
    startMin = IntegerField(min_value=0)
    startMax = IntegerField(min_value=0)
    endMin = IntegerField(min_value=0)
    endMax = IntegerField(min_value=0)
    referenceBases = RegexField(r'^([ACGTN]+)$', required=True)
    alternateBases = RegexField(r'^([ACGTN]+)$')
    variantType = ChoiceField("DEL", "INS", "DUP", "INV", "CNV", "SNP", "MNP", "DUP:TANDEM", "DEL:ME", "INS:ME", "BND")
    assemblyId = RegexField(r'^((GRCh|hg)[0-9]+([.]?p[0-9]+)?)$', required=True) # GRCh007.p9 is valid
    # datasetIds = ListField(items=RegexField(r'^[^<>"/;%{}+=]*$'))
    datasets = DatasetsField()
    includeDatasetResponses = ChoiceField("ALL", "HIT", "MISS", "NONE", default="NONE")
    filters = ListField(items=RegexField(r'.*:.+=?>?<?[0-9]*$'))
    mateName = ChoiceField("1", "2", "3", "4", "5", "6", "7",
                           "8", "9", "10", "11", "12", "13", "14",
                           "15", "16", "17", "18", "19", "20",
                           "21", "22", "X", "Y", "MT")
    

    def correlate(self, req, values):
        # values is a namedtuple, with the above keys

        LOG.info('Further correlation for the query endpoint')
        if not values.variantType and not values.alternateBases:
            raise BeaconBadRequest("Either 'alternateBases' or 'variantType' is required")

        if values.variantType and values.alternateBases != "N":
            raise BeaconBadRequest("If 'variantType' is provided then 'alternateBases' must be empty or equal to 'N'")

        if not values.start:
            if values.end:
                raise BeaconBadRequest("'start' is required if 'end' is provided")
            elif not values.startMin and not values.startMax and not values.endMin and not values.endMax:
                raise BeaconBadRequest("Either 'start' or all of 'startMin', 'startMax', 'endMin' and 'endMax' are required")
            elif not values.startMin or not values.startMax or not values.endMin or not values.endMax:
                raise BeaconBadRequest("All of 'startMin', 'startMax', 'endMin' and 'endMax' are required")
        else:
            if values.startMin or values.startMax or values.endMin or values.startMax:
                raise BeaconBadRequest("'start' cannot be provided at the same time as 'startMin', 'startMax', 'endMin' and 'endMax'")
            if not values.end and values.referenceBases == "N":
                raise BeaconBadRequest("'referenceBases' cannot be 'N' if 'start' is provided and 'end' is missing")

        if values.variantType != 'BND' and values.end and values.end < values.start:
            raise BeaconBadRequest("'end' must be greater than 'start'")
        if values.endMin and values.endMin > values.endMax:
            raise BeaconBadRequest("'endMin' must be smaller than 'endMax'")
        if values.startMin and values.startMin > values.startMax:
            raise BeaconBadRequest("'startMin' must be smaller than 'startMax'") 

        if values.mateName:
            raise BeaconBadRequest("Queries using 'mateName' are not implemented (yet)")


# ----------------------------------------------------------------------------------------------------------------------
#                                         UTILITIES
# ----------------------------------------------------------------------------------------------------------------------

# def create_final_response(query_parameters, datasets):
#     """
#     Create the final response as the Beacon Schema expects. 
#     """
#     # We create the final dictionary with all the info we want to return
#     beacon_response = { 'beaconId': conf.beacon_id,
#                         'apiVersion': conf.api_version,
#                         'exists': any([x['exists'] for x in datasets]),
#                         'info': None,
#                         'alleleRequest': query_parameters,
#                         'datasetAlleleResponses': filter_exists(query_parameters.includeDatasetResponses, datasets)}
    
#     # Before returning the response we need to filter it depending on the access levels
#     return {"beaconAlleleResponse": beacon_response}


# async def fetch_resulting_datasets(qparams, misses=False, accessible_missing=None):
#     """
#     Contact the DB to fetch the information about the datasets. 
#     :misses: set to True for retrieving data about datasets without the queried variant
#     :accessible_missing: list of accessible datasets without the variant.
#     Returns list of datasets dictionaries. 
#     """
#     async with pool.connection() as connection:
#         datasets = []
#         if misses:
#             if accessible_missing:
#                 dollars = ", ".join([ f"${i}" for i in range(1, len(accessible_missing)+1)])
#                 query = f"""SELECT id as "datasetId",
#                                    access_type as "accessType", stable_id as "stableId"
#                             FROM {conf.database_schema}.beacon_dataset
#                             WHERE id IN ({dollars});"""
#                 # LOG.debug(f"QUERY to fetch accessible missing info: {query}")
#                 statement = await connection.prepare(query)
#                 db_response =  await statement.fetch(*accessible_missing)
#             else:
#                 return []
#         else:
#             dollars = ", ".join([ f"${i}" for i in range(1, 14)]) # 1..13
#             query = f"""SELECT * FROM {conf.database_schema}.query_data_summary_response({dollars});"""
#             LOG.debug(f"QUERY to fetch hits: {query}")
#             statement = await connection.prepare(query)
#             db_response = await statement.fetch(qparams.variantType,
# 	                                        qparams.start,
# 	                                        qparams.startMin,
# 	                                        qparams.startMax,
# 	                                        qparams.end,
# 	                                        qparams.endMin,
# 	                                        qparams.endMax,
# 	                                        qparams.referenceName,
# 	                                        qparams.referenceBases,
# 	                                        qparams.alternateBases,
# 	                                        qparams.assemblyId,
# 	                                        qparams.datasets, # list of str
# 	                                        qparams.filters) # filters as-is

#         for record in list(db_response):
#             processed = transform_misses(record) if misses else await transform_record(db_pool, record)
#             datasets.append(processed)
#         return datasets


# async def get_datasets(query_parameters):
#     """
#     Find datasets based on query parameters.
#     """
#     hit_datasets = []
#     miss_datasets = []
#     response = []

#     # Fetch datasets where the variant is found
#     hit_datasets = await fetch_resulting_datasets(query_parameters)

#     # If the response has to include the datasets where the variant is not found, 
#     # we want to fetch info about them and shape them to be shown
#     if query_parameters.includeDatasetResponses in ['ALL', 'MISS']:
#         LOG.debug("datasets: %s", query_parameters.datasets)
#         _hits = set(d["internalId"] for d in hit_datasets)
#         LOG.debug("list_hits: %s", _hits)
#         accessible_missing = query_parameters.datasets - _hits
#         LOG.debug("accessible_missing: %s", accessible_missing)
#         miss_datasets = await fetch_resulting_datasets(db_pool,
#                                                        query_parameters,
#                                                        misses=True,
#                                                        accessible_missing=accessible_missing)
#     response = hit_datasets + miss_datasets
#     return response

# ----------------------------------------------------------------------------------------------------------------------
#                                         HANDLER
# ----------------------------------------------------------------------------------------------------------------------

proxy = QueryParameters()

async def handler(request):
    """
    Use the HTTP protocol 'GET' to return a Json object of a response to a given QUERY.
    It uses the '/query' path and expects some parameters.
    """
    LOG.info('Running a query request')
    qparams_raw, qparams_db = await proxy.fetch(request)
    LOG.debug("Original Query Parameters: %s", qparams_raw)

    # print only for debug
    if LOG.isEnabledFor(logging.DEBUG):
        print_qparams(qparams_db, proxy, LOG)

    response = dict(qparams_raw)

    # # 1. GET VALID/ACCESSIBLE DATASETS

    ###########
    ########### Daz: Commented out, cuz needs to be updated
    ###########
    # # We want to get a list of the datasets available in the database separated in three lists
    # # depending on the access level (we check all of them if the user hasn't specified anything, if some
    # # there were given, those are the only ones that are checked)
    # public_datasets, registered_datasets, controlled_datasets = [], [], []
    # async for access_type, dataset_id, _ in fetch_datasets_access(datasets=qparams_db.datasets[0]):
    #     if access_type == 'PUBLIC':
    #         public_datasets.append(dataset_id)
    #     elif access_type == 'REGISTERED':
    #         registered_datasets.append(dataset_id)
    #     elif access_type == 'CONTROLLED':
    #         controlled_datasets.append(dataset_id)

    # ##### TEST CODE TO USE WHEN AAI is integrated
    # # access_type, accessible_datasets = access_resolution(request, request['token'], request.host, public_datasets,
    # #                                                      registered_datasets, controlled_datasets)
    # # LOG.info(f"The user has this types of access: {access_type}")
    # # query_parameters[-2] = ",".join([str(id) for id in accessible_datasets])
    # ##### END TEST

    # # NOTE that right now we will just focus on the PUBLIC ones to ease the process, so we get all their 
    # # ids and add them to the query
    # datasetIds = set(public_datasets) # set of int
    # LOG.debug('Dataset Ids: %s', datasetIds)
    ###########
    ########### Daz: until here
    ###########
    ########### Reason: datasets are now resolved. qparams.datasets[0] is exactly the list of datasets
    ###########         the user has access to. If there is no user, the dataset will deal with the public datasets
    ###########         or intersect the public ones with the requested ones
    ###########

    # 3. RETRIEVE DATA FROM THE DB (use SQL function)

    #datasets = await get_datasets(qparams_db)
    LOG.info('Query done.')

    # # 5. CREATE FINAL RESPONSE
    
    # LOG.info('Creating the final response.')
    # beacon_response = create_final_response(query_parameters, datasets)
    
    # # 6. FILTER FINAL RESPONSE

    # # NOTE we hardcode accessible_datasets and user_levels it because authentication is not implemented yet
    # accessible_datasets = public_datasets
    # user_levels = ["PUBLIC"]  
    # filtered_response = filter_response(beacon_response, ACCESS_LEVELS_DICT, accessible_datasets, user_levels, query2access)
    # LOG.info('Done.')

    # response = filtered_response["beaconAlleleResponse"]

    return json_response(response)
