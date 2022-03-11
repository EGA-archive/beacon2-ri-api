from typing import Set
import re

import pymongo
from tqdm import tqdm

client = pymongo.MongoClient("mongodb://root:example@127.0.0.1:27017/beacon?authSource=admin")

def insert_set(ontology_terms):
    for term in ontology_terms:
        client.beacon.filtering_terms.insert_one({
            "type": "OntologyTerm",
            "id": term
        })

def find_all_ontology_terms_used() -> Set[str]:
    ontologies = set()
    for c_name in ["analyses", "biosamples", "cohorts", "genomicVariations", "datasets", "individuals", "runs"]:
        ontologies_aux = find_ontology_terms_used(c_name)
        ontologies = ontologies.union(ontologies_aux)
    return ontologies

def find_ontology_terms_used(collection_name: str) -> Set[str]:
    terms = set()
    rgx = re.compile(r"[_A-Za-z]+:\w+")
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    xs = client.beacon.get_collection(collection_name).find()
    for r in tqdm(xs, total=count):
        matches = rgx.findall(str(r))
        for match in matches:
            terms.add(match)
    return terms

tts = find_all_ontology_terms_used()
insert_set(tts)