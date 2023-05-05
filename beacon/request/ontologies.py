import re
import fastobo
import networkx
import requests
from beacon.request.model import Similarity
from pronto.ontology import Ontology
from os import scandir, listdir
from pathlib import Path

from owlready2 import OwlReadyOntologyParsingError
from tqdm import tqdm
from typing import Dict, Optional, Set, List
from beacon.db import client
from beacon import conf
import owlready2
import logging

LOG = logging.getLogger(__name__)

ONTOLOGIES = {"NCIT":"hola"}
ONTOLOGY_REGEX = re.compile(r"([_A-Za-z]+):(\w+)")

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
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    xs = client.beacon.get_collection(collection_name).find()
    for r in tqdm(xs, total=count):
        matches = ONTOLOGY_REGEX.findall(str(r))
        for match0, _ in matches:
            ontologies.add(match0)
    return ontologies


def find_ontology_terms_used(collection_name: str) -> Set[str]:
    terms = set()
    count = client.beacon.get_collection(collection_name).estimated_document_count()
    xs = client.beacon.get_collection(collection_name).find()
    for r in tqdm(xs, total=count):
        matches = ONTOLOGY_REGEX.findall(str(r))
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

def try_convert_owl_to_obo():
    ontology_directory = conf.ontologies_folder
    count = len(listdir(ontology_directory))
    for i, filename in enumerate(tqdm(scandir(ontology_directory), total=count)):
        new_filename = Path(filename.path).with_suffix(".obo")
        if filename.is_file() and filename.name.lower().endswith(".owl") and not new_filename.exists():
            LOG.debug("Transforming {} to {}".format(filename.path, new_filename))
            owl_onto: Ontology = Ontology(filename.path)
            with open(new_filename, "wb") as f:
                owl_onto.dump(f, format="obo")


def load_obo():
    try_convert_owl_to_obo()
    ontology_directory = conf.ontologies_folder
    count = len(listdir(ontology_directory))
    for i, filename in enumerate(tqdm(scandir(ontology_directory), total=count)):
        if filename.is_file() and filename.name.lower().endswith(".obo"):
            try:
                LOG.debug("Loading ontology {} of {} ({})".format(i, count, filename.name[:-4]))
                ONTOLOGIES[filename.name[:-4]] = fastobo.load(filename.path)
                LOG.debug(ONTOLOGIES[filename.name[:-4]] is None)
            except:
                LOG.error("Loading ontology {} failed".format(filename))


def get_descendants(term: str) -> List[str]:

    ontology_id, term_id = term.split(':')

    # Create ontology graph
    # TODO: Cache should be the graph
    knowledge_graph = networkx.DiGraph()
    for frame in ONTOLOGIES[ontology_id]:
        if isinstance(frame, fastobo.term.TermFrame):
            knowledge_graph.add_node(str(frame.id))
            for clause in frame:
                if isinstance(clause, fastobo.term.IsAClause):
                    knowledge_graph.add_edge(str(frame.id), str(clause.term))
    print(networkx.is_directed_acyclic_graph(knowledge_graph))

    return list(networkx.descendants(knowledge_graph, term))


def get_ontology_neighbours(term: str, depth: int) -> List[str]:
    ontology_id, term_id = term.split(':')
    LOG.debug(ONTOLOGIES)
    # Create ontology graph
    # TODO: Cache should be the graph
    knowledge_graph = networkx.DiGraph()
    
    for frame in ONTOLOGIES[ontology_id]:
        if isinstance(frame, fastobo.term.TermFrame):
            knowledge_graph.add_node(str(frame.id))
            for clause in frame:
                if isinstance(clause, fastobo.term.IsAClause):
                    knowledge_graph.add_edge(str(frame.id), str(clause.term))
    print(networkx.is_directed_acyclic_graph(knowledge_graph))
    LOG.debug(knowledge_graph)
    # Get predecessors
    first_predecessors = set(knowledge_graph.predecessors(term))

    # Get siblings
    siblings = set()
    for parent in first_predecessors:
        siblings = siblings.union(set(knowledge_graph.successors(parent)))

    # Get successors and predecessors with depth
    predecessors = set(knowledge_graph.predecessors(term))
    successors = set(knowledge_graph.successors(term))
    for _ in range(1, depth):
        for predecessor in predecessors:
            predecessors = predecessors.union(set(knowledge_graph.predecessors(predecessor)))
        for successor in successors:
            successors = successors.union(set(knowledge_graph.successors(successor)))

    # Combine results
    terms = set()
    terms.add(term)
    terms = terms.union(predecessors)
    terms = terms.union(siblings)
    terms = terms.union(successors)

    return list(terms)

def get_similar_ontology_terms(term: str, similarity: Similarity) -> List[str]:
    if similarity == Similarity.EXACT:
        return [term]
    elif similarity == Similarity.HIGH:
        return get_ontology_neighbours(term, depth=1)
    elif similarity == Similarity.MEDIUM:
        return get_ontology_neighbours(term, depth=2)
    else:
        # similarity == Similarity.LOW
        return get_ontology_neighbours(term, depth=3)


def get_ontology_config(ontology: owlready2.Ontology) -> Optional[Dict]:
    ontology_url = "https://www.ebi.ac.uk/ols/api/ontologies/{}".format(ontology.name)
    try:
        return requests.get(ontology_url).json()["config"]
    except:
        return None

def get_resources() -> List[Dict]:
    resources = []
    for onto in ONTOLOGIES.values():
        ontology_config = get_ontology_config(onto)
        resources.append({ 
            "id": onto.name,
            "name": ontology_config["title"] if ontology_config else onto.name,
            "url": ontology_config["id"] if ontology_config else onto.base_iri,
            "version": ontology_config["version"] if ontology_config else None,
            "nameSpacePrefix": ontology_config["namespace"].upper() if ontology_config else None,
            "iriPrefix": ontology_config["baseUris"][0] if ontology_config else None,
        })
    return resources