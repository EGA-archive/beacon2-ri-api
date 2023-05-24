from pymongo.mongo_client import MongoClient
import logging
import json


LOG = logging.getLogger(__name__)

def get_count(collection, query: dict) -> int:
    if not query:
        LOG.debug("Returning estimated count")
        return collection.estimated_document_count()
    else:
        LOG.debug("FINAL QUERY (COUNT): {}".format(query))
        LOG.debug("Returning count")
        return collection.count_documents(query)

client = MongoClient(
    #"mongodb://127.0.0.1:27017/"
    "mongodb://root:example@mongo:27017/beacon?authSource=admin"

)


ethnicities =  {    "African" : 119,
                    "Any other Asian background" : 120,
                    "Any other Black background" : 104,
                    "Any other mixed background" : 92,
                    "Any other white background" : 114,
                    "Asian or Asian British" : 125,
                    "Bangladeshi" : 96,
                    "Black or Black British" : 131,
                    "British" : 114,
                    "Caribbean" : 127,
                    "Chinese" : 100,
                    "Indian" : 110,
                    "Irish" : 111,
                    "Mixed" : 127,
                    "Other ethnic group" : 116,
                    "Pakistani" : 115,
                    "White" : 105,
                    "White and Asian" : 114,
                    "White and Black African" : 115,
                    "White and Black Caribbean" : 132}

genders = {
                    "female" : 1271,
                    "male" : 1233
                 }

diseases = {
                    "acute bronchitis" : 121,
                    "agranulocytosis" : 111,
                    "asthma" : 134,
                    "bipolar affective disorder" : 134,
                    "cardiomyopathy" : 133,
                    "dental caries" : 139,
                    "eating disorders" : 134,
                    "fibrosis and cirrhosis of liver" : 132,
                    "gastro-oesophageal reflux disease" : 140,
                    "haemorrhoids" : 127,
                    "influenza due to certain identified influenza virus" : 135,
                    "insulin-dependent diabetes mellitus" : 165,
                    "iron deficiency anaemia" : 142,
                    "multiple sclerosis" : 125,
                    "obesity" : 136,
                    "sarcoidosis" : 136,
                    "schizophrenia" : 138,
                    "thyroiditis" : 141,
                    "varicose veins of lower extremities" : 139
                 }

string_1 = ""
string_2 = ""
string_3 = ""
string_4 = ""




for k1,v1 in diseases.items():
    dict_3={}
    for k, v in genders.items():
        query_filtering={}
        query_filtering['$and']=[]
        query={}
        string_3 = k
        query['sex.label'] = string_3
        query_filtering['$and'].append(query)
        query={}
        string_1=k1
        query['diseases.diseaseCode.label'] = string_1
        query_filtering['$and'].append(query)
        count = get_count(client.beacon.individuals, query_filtering)
        dict_3[k]=count
        dict_2={}
        dict_2[k1]= dict_3
    string_dict = json.dumps(dict_2)
    path = 'diseases_sex.txt'
    with open(path, 'a+') as f:
        f.write(string_dict+"\n")
    f.close()

for k1,v1 in diseases.items():
    dict_3={}
    for k, v in ethnicities.items():
        query_filtering={}
        query_filtering['$and']=[]
        query={}
        string_3 = k
        query['ethnicity.label'] = string_3
        query_filtering['$and'].append(query)
        query={}
        string_1=k1
        query['diseases.diseaseCode.label'] = string_1
        query_filtering['$and'].append(query)
        count = get_count(client.beacon.individuals, query_filtering)
        dict_3[k]=count
        dict_2={}
        dict_2[k1]= dict_3
    string_dict = json.dumps(dict_2)
    path = 'diseases_eth.txt'
    with open(path, 'a+') as f:
        f.write(string_dict+"\n")
    f.close()

for k1,v1 in ethnicities.items():
    dict_3={}
    for k, v in diseases.items():
        query_filtering={}
        query_filtering['$and']=[]
        query={}
        string_3 = k
        query['diseases.diseaseCode.label'] = string_3
        query_filtering['$and'].append(query)
        query={}
        string_1=k1
        query['ethnicity.label'] = string_1
        query_filtering['$and'].append(query)
        count = get_count(client.beacon.individuals, query_filtering)
        dict_3[k]=count
        dict_2={}
        dict_2[k1]= dict_3
    string_dict = json.dumps(dict_2)
    path = 'eth_diseases.txt'
    with open(path, 'a+') as f:
        f.write(string_dict+"\n")
    f.close()


for k1,v1 in ethnicities.items():
    dict_3={}
    for k, v in genders.items():
        query_filtering={}
        query_filtering['$and']=[]
        query={}
        string_3 = k
        query['sex.label'] = string_3
        query_filtering['$and'].append(query)
        query={}
        string_1=k1
        query['ethnicity.label'] = string_1
        query_filtering['$and'].append(query)
        count = get_count(client.beacon.individuals, query_filtering)
        dict_3[k]=count
        dict_2={}
        dict_2[k1]= dict_3
    string_dict = json.dumps(dict_2)
    path = 'eth_sex.txt'
    with open(path, 'a+') as f:
        f.write(string_dict+"\n")
    f.close()