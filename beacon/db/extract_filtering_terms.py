import os.path
from typing import List, Dict, Optional
import re
from pymongo.mongo_client import MongoClient
import progressbar
from bson.objectid import ObjectId
from tqdm import tqdm
from bson.json_util import dumps
import json

import sys
import os


current = os.path.dirname(os.path.realpath(__file__))


parent = os.path.dirname(current)


sys.path.append(parent)


import conf


ONTOLOGY_REGEX = re.compile(r"([_A-Za-z0-9]+):([_A-Za-z0-9^\-]+)")
ICD_REGEX = re.compile(r"(ICD[_A-Za-z0-9]+):([_A-Za-z0-9^\./-]+)")


client = MongoClient(
        #"mongodb://127.0.0.1:27017/"
        "mongodb://{}:{}@{}:{}/{}?authSource={}".format(
            conf.database_user,
            conf.database_password,
            conf.database_host,
            conf.database_port,
            conf.database_name,
            conf.database_auth_source,
        )
    )

'''
client = MongoClient(
client = MongoClient(
    #"mongodb://127.0.0.1:27017/"
    "mongodb://root:example@mongo:27017/beacon?authSource=admin"

)
'''

class MyProgressBar:
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num: int, block_size: int, total_size: int):
        if not self.pbar:
            self.pbar = progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def get_ontology_field_name(ontology_id:str, term_id:str, collection:str):
    biosamples=['biosampleStatus.id','diagnosticMarkers.id','histologicalDiagnosis.id','measurements.assayCode.id','measurements.measurementValue.id','measurements.measurementValue.referenceRange.unit.id','measurements.measurementValue.typedQuantities.quantity.unit.id','measurements.measurementValue.unit.id','measurements.observationMoment.id','measurements.procedure.bodySite.id','measurements.procedure.procedureCode.id','pathologicalStage.id','pathologicalTnmFinding.id','phenotypicFeatures.evidence.evidenceCode.id','phenotypicFeatures.evidence.reference.id','phenotypicFeatures.featureType.id','phenotypicFeatures.modifiers.id','phenotypicFeatures.onset.id','phenotypicFeatures.resolution.id','phenotypicFeatures.severity.id','sampleOriginDetail.id','sampleOriginType.id','sampleProcessing.id','sampleStorage.id','tumorGrade.id','tumorProgression.id']
    cohorts=['cohortDataTypes.id','cohortDesign.id','exclusionCriteria.diseaseConditions.diseaseCode.id','exclusionCriteria.diseaseConditions.severity.id','exclusionCriteria.diseaseConditions.stage.id','exclusionCriteria.ethnicities.id','exclusionCriteria.genders.id','exclusionCriteria.locations.id','exclusionCriteria.phenotypicConditions.featureType.id','exclusionCriteria.phenotypicConditions.severity.id','inclusionCriteria.diseaseConditions.diseaseCode.id','inclusionCriteria.diseaseConditions.severity.id','inclusionCriteria.diseaseConditions.stage.id','inclusionCriteria.ethnicities.id','inclusionCriteria.genders.id','inclusionCriteria.locations.id','inclusionCriteria.phenotypicConditions.featureType.id','inclusionCriteria.phenotypicConditions.severity.id']
    datasets=['dataUseConditions.duoDataUse.id']
    genomicVariations=['caseLevelData.alleleOrigin.id','caseLevelData.clinicalInterpretations.category.id','caseLevelData.clinicalInterpretations.effect.id','caseLevelData.clinicalInterpretations.evidenceType.id','caseLevelData.id','caseLevelData.phenotypicEffects.category.id','caseLevelData.phenotypicEffects.effect.id','caseLevelData.phenotypicEffects.evidenceType.id','caseLevelData.zygosity.id','identifiers.variantAlternativeIds.id','molecularAttributes.molecularEffects.id','variantLevelData.clinicalInterpretations.category.id','variantLevelData.clinicalInterpretations.effect.id','variantLevelData.clinicalInterpretations.evidenceType.id','variantLevelData.phenotypicEffects.category.id','variantLevelData.phenotypicEffects.effect.id','variantLevelData.phenotypicEffects.evidenceType.id']
    individuals=['diseases.ageOfOnset.id','diseases.diseaseCode.id','diseases.severity.id','diseases.stage.id','ethnicity.id','exposures.exposureCode.id','exposures.unit.id','geographicOrigin.id','interventionsOrProcedures.ageAtProcedure.id','interventionsOrProcedures.bodySite.id','interventionsOrProcedures.procedureCode.id','measures.assayCode.id','measures.measurementValue.id','measures.measurementValue.typedQuantities.quantity.unit.id','measures.measurementValue.unit.id','measures.observationMoment.id','measures.procedure.bodySite.id','measures.procedure.procedureCode.id','pedigrees.disease.diseaseCode.id','pedigrees.disease.severity.id','pedigrees.disease.stage.id','pedigrees.id','pedigrees.members.role.id','phenotypicFeatures.evidence.evidenceCode.id','phenotypicFeatures.evidence.reference.id','phenotypicFeatures.featureType.id','phenotypicFeatures.modifiers.id','phenotypicFeatures.onset.id','phenotypicFeatures.resolution.id','phenotypicFeatures.severity.id','sex.id','treatments.cumulativeDose.referenceRange.id','treatments.doseIntervals.id','treatments.routeOfAdministration.id','treatments.treatmentCode.id']
    runs=['librarySource.id','platformModel.id']
    array=[]
    if collection == 'biosamples':
        array=biosamples
    elif collection == 'cohorts':
        array=cohorts
    elif collection == 'datasets':
        array=datasets
    elif collection == 'genomicVariations':
        array=genomicVariations
    elif collection == 'individuals':
        array=individuals
    elif collection == 'runs':
        array=runs
    query={}
    query['$or']=[]
    for field in array:
        fieldquery={}
        fieldquery[field]=ontology_id + ":" + term_id
        query['$or'].append(fieldquery)
    results = client.beacon.get_collection(collection).find(query).limit(1)
    results = list(results)
    results = dumps(results)
    results = json.loads(results)
    field = ''
    for result in results:
        for k, v in result.items():
            if isinstance(v, str): 
                if v == ontology_id + ':' + term_id:
                    field = k
                    for key, value in result.items():
                        if key == 'label':
                            label = value
                        break
                    break
            elif isinstance(v, dict):
                for k2, v2 in v.items():
                    if isinstance(v2, list):
                        for item_list in v2:
                            if isinstance(item_list, str): 
                                if item_list == ontology_id + ':' + term_id:
                                    field = k + '.' + k2
                                    for key, value in v.items():
                                        if key == 'label':
                                            label = value
                                            break
                                    break
                            elif isinstance(item_list, dict):
                                for k21, v21 in item_list.items():
                                    if isinstance(v21, str):
                                        if v21 == ontology_id + ':' + term_id:
                                            field = k + '.' + k2 + '.' + k21
                                            for key, value in item_list.items():
                                                if key == 'label':
                                                    label = value
                                                    break
                                            break
                                    elif isinstance(v21,dict):
                                        for k22, v22 in v21.items():
                                            if v22 == v21 == ontology_id + ':' + term_id:
                                                field = k + '.' + k2 + '.' + k22
                                                for key, value in v21.items():
                                                    if key == 'label':
                                                        label = value
                                                        break
                                                break
                    elif v2 == ontology_id + ':' + term_id:
                        field = k + '.' + k2
                        for key, value in v.items():
                            if key == 'label':
                                label = value
                                break
                        break
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, str): 
                        if item == ontology_id + ':' + term_id:
                            field = k
                            for key, value in result.items():
                                if key == 'label':
                                    label = value
                                    break
                            break
                    elif isinstance(item, dict):
                        for k2, v2 in item.items():
                            if isinstance(v2, str):
                                if v2 == ontology_id + ':' + term_id:
                                    field = k + '.' + k2
                                    for key, value in item.items():
                                        if k == 'label':
                                            label = v
                                            break
                                    break
                            elif isinstance(v2, dict):
                                for k3, v3 in v2.items():
                                    if isinstance(v3, str):
                                        if v3 == ontology_id + ':' + term_id:
                                            field = k + '.' + k2 + '.' + k3
                                            for key, value in v2.items():
                                                if key == 'label':
                                                    label = value
                                                    break
                                            break 
                                    elif isinstance(v3, dict):
                                        for k4, v4 in v3.items():
                                            if isinstance(v4, str):
                                                if v4 == ontology_id + ':' + term_id:
                                                    field = k + '.' + k2 + '.' + k3 + '.' + k4
                                                    for key, value in v3.items():
                                                        if key == 'label':
                                                            label = value
                                                            break
                                                    break 
                                            elif isinstance(v4, dict):
                                                for k5, v5 in v4.items():
                                                    if v5 == ontology_id + ':' + term_id:
                                                        field = k + '.' + k2 + '.' + k3 + '.' + k4 + '.' + k5
                                                        for key, value in v4.items():
                                                            if key == 'label':
                                                                label = value
                                                                break
                                                        break 


        if '.' in field:
            try:
                final_field = ''
                field_split = field.split('.')
                del field_split[-1]
                for item in field_split:
                    if final_field == '':
                        final_field = item
                    else:
                        final_field = final_field + '.' + item
                final_dict={}
                final_dict['field']=final_field
                final_dict['label']=label
                return final_dict
            except Exception:
                pass
        else:
            pass


def insert_all_ontology_terms_used():
    collections = client.beacon.list_collection_names()
    if 'filtering_terms' in collections:
        collections.remove('filtering_terms')
    print("Collections:", collections)
    for c_name in collections:
        if c_name not in ['counts', 'similarities', 'synonyms']:
            terms_ids = find_ontology_terms_used(c_name)
            terms = get_filtering_object(terms_ids, c_name)
            if len(terms) > 0:
                client.beacon.filtering_terms.insert_many(terms)

def find_ontology_terms_used(collection_name: str) -> List[Dict]:
    print(collection_name)
    terms_ids = []
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    if count < 10000:
        num_total=count
    else:
        num_total=10000
    i=0
    if count > 10000:
        while i < count:
            xs = client.beacon.get_collection(collection_name).find().skip(i).limit(10000)
            for r in tqdm(xs, total=num_total):
                matches = ONTOLOGY_REGEX.findall(str(r))
                icd_matches = ICD_REGEX.findall(str(r))
                for ontology_id, term_id in matches:
                    term = ':'.join([ontology_id, term_id])
                    if term not in terms_ids:
                        terms_ids.append(term)
                for ontology_id, term_id in icd_matches:
                    term = ':'.join([ontology_id, term_id])
                    if term not in terms_ids:
                        terms_ids.append(term)
            i += 10000
            if i > 30000:
                break
            print(i)
    else:
        xs = client.beacon.get_collection(collection_name).find().skip(0).limit(10000)
        for r in tqdm(xs, total=num_total):
            matches = ONTOLOGY_REGEX.findall(str(r))
            icd_matches = ICD_REGEX.findall(str(r))
            for ontology_id, term_id in matches:
                term = ':'.join([ontology_id, term_id])
                if term not in terms_ids:
                    terms_ids.append(term) 
            for ontology_id, term_id in icd_matches:
                term = ':'.join([ontology_id, term_id])
                if term not in terms_ids:
                    terms_ids.append(term)

    return terms_ids



def get_filtering_object(terms_ids: list, collection_name: str):
    terms = []
    list_of_ontologies=[]
    #ontologies = dict()
    for onto in terms_ids:
        ontology = onto.split(':')
        ontology_id = ontology[0]
        term_id = ontology[1]
        #if ontology_id not in ontologies:
            #ontologies[ontology_id] = load_ontology(ontology_id)
        if ontology_id.isupper():
            field_dict = get_ontology_field_name(ontology_id, term_id, collection_name)
        else:
            continue
        try:
            field = field_dict['field']
            label = field_dict['label']
            value_id=None
            if 'measurements.assayCode' in field:
                value_id = label
            else:
                ontology_label = label
            if field is not None:
                if onto not in list_of_ontologies:
                    list_of_ontologies.append(onto)
                    if label:
                        terms.append({
                                        'type': 'ontology',
                                        'id': onto,
                                        'label': ontology_label,
                                        # TODO: Use conf.py -> beaconGranularity to not disclouse counts in the filtering terms
                                        #'count': get_ontology_term_count(collection_name, onto),
                                        'scopes': [collection_name[0:-1]]                 
                                    })

                        terms.append({
                                                'type': 'alphanumeric',
                                                'id': field,
                                                # TODO: Use conf.py -> beaconGranularity to not disclouse counts in the filtering terms
                                                #'count': get_ontology_term_count(collection_name, onto),
                                                'scopes': [collection_name[0:-1]]     
                                            })
                        terms.append({
                                        'type': 'custom',
                                        'id': '{}:{}'.format(field,label),
                                        # TODO: Use conf.py -> beaconGranularity to not disclouse counts in the filtering terms
                                        #'count': get_ontology_term_count(collection_name, onto),
                                        'scopes': [collection_name[0:-1]]                        
                                    })
                    if value_id is not None:
                        terms.append({
                                                'type': 'alphanumeric',
                                                'id': value_id,
                                                # TODO: Use conf.py -> beaconGranularity to not disclouse counts in the filtering terms
                                                #'count': get_ontology_term_count(collection_name, onto),
                                                'scopes': [collection_name[0:-1]]     
                                            })

                print(terms)
        except Exception:
            pass

    return terms


def get_alphanumeric_term_count(collection_name: str, key: str) -> int:
    return len(client.beacon\
        .get_collection(collection_name)\
        .distinct(key))

def get_properties_of_document(document, prefix="") -> List[str]:
    properties = []
    if document is None or isinstance(document, str) or isinstance(document, int):
        return []
    elif isinstance(document, list):
        for elem in document:
            properties += get_properties_of_document(elem, prefix)
    elif isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                continue
            elif value is None:
                properties.append(prefix + '.' + key if prefix else key)
            elif isinstance(value, int):
                properties.append(prefix + '.' + key if prefix else key)
            elif isinstance(value, str):
                properties.append(prefix + '.' + key if prefix else key)
            elif isinstance(value, list):
                properties += get_properties_of_document(value, prefix + '.' + key if prefix else key)
            elif isinstance(value, dict):
                properties += get_properties_of_document(value, prefix + '.' + key if prefix else key)
            else:
                print('Unknown type:', value, ' (', type(value), ')')
                exit(0)
    else:
        print('Unknown type2:', document, ' (', type(document), ')')
        exit(0)
    return properties

def merge_ontology_terms():
    filtering_terms = client.beacon.filtering_terms.find({"type": "ontology"})
    array_of_ids=[]
    repeated_ids=[]
    new_terms=[]
    for filtering_term in filtering_terms:
        new_id=filtering_term["id"]
        if new_id not in array_of_ids:
            array_of_ids.append(new_id)
        else:
            repeated_ids.append(new_id)
    #print("repeated_ids are {}".format(repeated_ids))
    for repeated_id in repeated_ids:
        repeated_terms = client.beacon.filtering_terms.find({"id": repeated_id, "type": "ontology"})
        array_of_scopes=[]
        for repeated_term in repeated_terms:
            #print(repeated_term)
            id=repeated_term["id"]
            label=repeated_term["label"]
            if repeated_term['scopes'] != []:
                if repeated_term['scopes'][0] not in array_of_scopes:
                    array_of_scopes.append(repeated_term['scopes'][0])
        if array_of_scopes != []:
            new_terms.append({
                'type': 'ontology',
                'id': id,
                'label': label,
                # TODO: Use conf.py -> beaconGranularity to not disclouse counts in the filtering terms
                #'count': get_ontology_term_count(collection_name, onto),
                'scopes': array_of_scopes        
                        })
        client.beacon.filtering_terms.delete_many({"id": repeated_id})
    if new_terms != []:
        client.beacon.filtering_terms.insert_many(new_terms)
        
    
def merge_alphanumeric_terms():
    filtering_terms = client.beacon.filtering_terms.find({"type": "alphanumeric"})
    array_of_ids=[]
    repeated_ids=[]
    new_terms=[]
    for filtering_term in filtering_terms:
        new_id=filtering_term["id"]
        if new_id not in array_of_ids:
            array_of_ids.append(new_id)
        else:
            repeated_ids.append(new_id)
    #print("repeated_ids are {}".format(repeated_ids))
    for repeated_id in repeated_ids:
        repeated_terms = client.beacon.filtering_terms.find({"id": repeated_id, "type": "alphanumeric"})
        array_of_scopes=[]
        for repeated_term in repeated_terms:
            #print(repeated_term)
            id=repeated_term["id"]
            if repeated_term['scopes'] != []:
                if repeated_term['scopes'][0] not in array_of_scopes:
                    array_of_scopes.append(repeated_term['scopes'][0])
        if array_of_scopes != []:
            new_terms.append({
                'type': 'alphanumeric',
                'id': id,
                # TODO: Use conf.py -> beaconGranularity to not disclouse counts in the filtering terms
                #'count': get_ontology_term_count(collection_name, onto),
                'scopes': array_of_scopes        
                        })
        client.beacon.filtering_terms.delete_many({"id": repeated_id})
    if new_terms != []:
        client.beacon.filtering_terms.insert_many(new_terms)
    
def merge_custom_terms():
    filtering_terms = client.beacon.filtering_terms.find({"type": "custom"})
    array_of_ids=[]
    repeated_ids=[]
    new_terms=[]
    for filtering_term in filtering_terms:
        new_id=filtering_term["id"]
        if new_id not in array_of_ids:
            array_of_ids.append(new_id)
        else:
            repeated_ids.append(new_id)
    #print("repeated_ids are {}".format(repeated_ids))
    for repeated_id in repeated_ids:
        repeated_terms = client.beacon.filtering_terms.find({"id": repeated_id, "type": "custom"})
        array_of_scopes=[]
        for repeated_term in repeated_terms:
            #print(repeated_term)
            id=repeated_term["id"]
            if repeated_term['scopes'] != []:
                if repeated_term['scopes'][0] not in array_of_scopes:
                    array_of_scopes.append(repeated_term['scopes'][0])
        if array_of_scopes != []:
            new_terms.append({
                'type': 'custom',
                'id': id,
                # TODO: Use conf.py -> beaconGranularity to not disclouse counts in the filtering terms
                #'count': get_ontology_term_count(collection_name, onto),
                'scopes': array_of_scopes        
                        })
        client.beacon.filtering_terms.delete_many({"id": repeated_id})
    if new_terms != []:
        client.beacon.filtering_terms.insert_many(new_terms)




insert_all_ontology_terms_used()
merge_ontology_terms()
merge_alphanumeric_terms()
merge_custom_terms()