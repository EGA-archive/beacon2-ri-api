import os.path
import urllib.request
from typing import List, Dict, Optional
import re
from urllib.error import HTTPError

import owlready2
from pymongo.mongo_client import MongoClient
import progressbar
from bson.objectid import ObjectId
from owlready2 import OwlReadyOntologyParsingError
from tqdm import tqdm
from beacon import conf

from beacon.request.ontologies import ONTOLOGY_REGEX

client = MongoClient(
    "mongodb://{}:{}@{}:{}/{}?authSource={}".format(
        conf.database_user,
        conf.database_password,
        conf.database_host,
        conf.database_port,
        conf.database_name,
        conf.database_auth_source,
    )
)

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


def insert_all_ontology_terms_used():
    collections = client.beacon.list_collection_names()
    if 'filtering_terms' in collections:
        collections.remove('filtering_terms')
    print("Collections:", collections)
    for c_name in collections:
        terms = find_ontology_terms_used(c_name)
        if len(terms) > 0:
            client.beacon.filtering_terms.insert_many(terms)


def get_ontology_name(ontology: owlready2.Ontology) -> str:
    return ontology.name


def load_ontology_obo(ontology_id: str) -> Optional[owlready2.Ontology]:
    if ontology_id.isalpha():
        url = "https://www.ebi.ac.uk/{}/{}.obo".format(ontology_id.lower(), ontology_id.lower())
        path = "ontologies/{}.obo".format(ontology_id)
        try:
            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path, MyProgressBar())
            return owlready2.get_ontology(path).load()
        except HTTPError:
            # TODO: Handle error
            print("ERROR", HTTPError)
            pass
        except OwlReadyOntologyParsingError:
            # TODO: Handle error
            pass

def load_ontology(ontology_id: str) -> Optional[owlready2.Ontology]:
    if ontology_id.isalpha():
        url = "https://www.ebi.ac.uk/ols/ontologies/{}/download".format(ontology_id)
        path = "ontologies/{}.owl".format(ontology_id)
        try:
            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path, MyProgressBar())
            return owlready2.get_ontology(path).load()
        except HTTPError:
            # TODO: Handle error
            print("ERROR", HTTPError)
            pass
        except OwlReadyOntologyParsingError:
            # TODO: Handle error
            pass


def get_ontology_term_label(ontology: owlready2.Ontology, term: str) -> Optional[str]:
    ontology_class_name = term.replace(':', '_')
    res = ontology.search(iri="*{}".format(ontology_class_name))
    for c in res:
        if c.name == ontology_class_name:
            if len(c.label) > 0:
                return c.label.first()
            else:
                return c.name
    return None


def get_ontology_term_count(collection_name: str, term: str) -> int:
    query = {
        '$text': {
            '$search': term
        }
    }
    return client.beacon\
        .get_collection(collection_name)\
        .count_documents(query)


def find_ontology_terms_used(collection_name: str) -> List[Dict]:
    terms = []
    terms_ids = set()
    ontologies = dict()
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    xs = client.beacon.get_collection(collection_name).find()
    for r in tqdm(xs, total=count):
        matches = ONTOLOGY_REGEX.findall(str(r))
        for ontology_id, term_id in matches:
            term = ':'.join([ontology_id, term_id])
            print(term, ontology_id)
            if term not in terms_ids:
                terms_ids.add(term)
                if ontology_id not in ontologies:
                    ontologies[ontology_id] = load_ontology(ontology_id)
                if ontologies[ontology_id] is not None:
                    terms.append({
                        'type': get_ontology_name(ontologies[ontology_id]),
                        'id': term,
                        'label': get_ontology_term_label(ontologies[ontology_id], term),
                        # TODO: Use conf.py -> beaconGranularity to not disclouse counts in the filtering terms
                        'count': get_ontology_term_count(collection_name, term),
                        'collection': collection_name,
                    })
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


def find_alphanumeric_terms_used(collection_name: str) -> List[Dict]:
    terms = []
    terms_ids = set()
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    xs = client.beacon.get_collection(collection_name).find()
    for r in tqdm(xs, total=count):
        properties = get_properties_of_document(r)
        for p in properties:
            if p not in terms_ids:
                terms_ids.add(p)
                terms.append({
                    'type': 'alphanumeric',
                    'id': p,
                    'count': get_alphanumeric_term_count(collection_name, p),
                    'collection': collection_name,
                })
    return terms


def insert_all_alphanumeric_terms_used():
    collections = client.beacon.list_collection_names()
    if 'filtering_terms' in collections:
        collections.remove('filtering_terms')
    print("Collections:", collections)
    for c_name in collections:
        terms = find_alphanumeric_terms_used(c_name)
        print(terms)
        if len(terms) > 0:
            client.beacon.filtering_terms.insert_many(terms)


insert_all_ontology_terms_used()
insert_all_alphanumeric_terms_used()
