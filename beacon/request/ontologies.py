import re
from os import scandir, listdir

from owlready2 import OwlReadyOntologyParsingError
from tqdm import tqdm
from typing import Set, List
from beacon.db import client
from beacon import conf
import owlready2
import logging

LOG = logging.getLogger(__name__)

ONTOLOGIES = {}


def find_all_ontologies_used() -> Set[str]:
    ontologies = set()
    for c_name in ["analyses", "biosamples", "cohorts", "genomicVariations", "datasets", "individuals", "runs"]:
        ontologies_aux = find_ontologies_used(c_name)
        ontologies = ontologies.union(ontologies_aux)
    return ontologies


def find_all_ontology_terms_used() -> Set[str]:
    ontologies = set()
    for c_name in ["analyses", "biosamples", "cohorts", "genomicVariations", "datasets", "individuals", "runs"]:
        ontologies_aux = find_ontology_terms_used(c_name)
        ontologies = ontologies.union(ontologies_aux)
    return ontologies


def find_ontologies_used(collection_name: str) -> Set[str]:
    ontologies = set()
    rgx = re.compile(r"([_A-Za-z]+):(\w+)")
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    xs = client.beacon.get_collection(collection_name).find()
    for r in tqdm(xs, total=count):
        matches = rgx.findall(str(r))
        for match0, _ in matches:
            ontologies.add(match0)
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


def load():
    ontology_directory = conf.ontologies_folder
    owlready2.onto_path.append(ontology_directory)
    count = len(listdir(ontology_directory))
    for i, filename in enumerate(tqdm(scandir(ontology_directory), total=count)):
        if filename.is_file() and filename.name.lower().endswith(".owl"):
            try:
                LOG.debug("Loading ontology {} of {}".format(i, count))
                ONTOLOGIES[filename.name[:-4]] = owlready2.get_ontology(filename.path).load()
            except OwlReadyOntologyParsingError:
                # TODO: Add error
                continue


def get_descendants(filter_id: str) -> List[str]:
    descendants = []

    ontology_class_name = filter_id.replace(':', '_')
    ontology, _ = ontology_class_name.split('_')

    onto = ONTOLOGIES.get(ontology)
    if onto is not None:
        res = onto.search(iri="*{}".format(ontology_class_name))
        for c in res:
            if c.name == ontology_class_name:
                for descendant in onto.get_children_of(c):
                    descendants.append(descendant.name.replace('_', ':'))
    return descendants


def get_resources():
    resources = []
    for onto in ONTOLOGIES.values():
        resources.append({
            "id": onto.name,
            "url": onto.base_iri
        })
    return resources
