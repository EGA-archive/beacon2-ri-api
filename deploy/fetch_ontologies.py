# Query MongoDB to retrieve all of the ontologies used
from typing import Set
import re
from urllib.error import HTTPError
from pymongo.mongo_client import MongoClient

import urllib.request
import os
from tqdm import tqdm
import conf

ONTOLOGY_REGEX = re.compile(r"([_A-Za-z]+):(\w+)")

client = MongoClient(
    "mongodb://127.0.0.1:27017/")
def find_all_ontologies_used() -> Set[str]:
    ontologies = set()
    for c_name in ["analyses", "biosamples", "cohorts", "genomicVariations", "datasets", "individuals", "runs"]:
        ontologies_aux = find_ontologies_used(c_name)
        ontologies = ontologies.union(ontologies_aux)
    return ontologies


def find_ontologies_used(collection_name: str) -> Set[str]:
    terms = set()
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    xs = client.beacon.get_collection(collection_name).find()
    for r in tqdm(xs, total=count):
        matches = ONTOLOGY_REGEX.findall(str(r))
        for match0, match1 in matches:
            terms.add(match0)
    return terms


# Try to download each of the ontologies to the ontologies folder
list_of_ontologies = find_all_ontologies_used()

if len(list_of_ontologies) > 0 and not os.path.exists("ontologies"):
    os.mkdir("ontologies")

for ontology in tqdm(list_of_ontologies):
    if ontology.isalpha():
        url = "https://www.ebi.ac.uk/ols/ontologies/{}/download".format(ontology)
        path = "ontologies/{}.owl".format(ontology)
        try:
            response = urllib.request.urlretrieve(url, path)
        except HTTPError:
            continue
