import owlready2
import obonet
import networkx
import json
import os
from typing import List, Dict, Optional
import urllib.request
from urllib.error import HTTPError
import progressbar

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

def load_ontology(ontology_id: str) -> Optional[owlready2.Ontology]:
    if ontology_id.isalpha():
        url_alt = "https://www.ebi.ac.uk/efo/EFO.obo"
        url = "http://purl.obolibrary.org/obo/{}.obo".format(ontology_id.lower())
        path = "/beacon/beacon/db/ontologies/{}.obo".format(ontology_id)
        try:
            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path, MyProgressBar())
        except HTTPError:
            # TODO: Handle error
            print("ERROR", HTTPError)
            pass
        except ValueError:
            print("ERROR", ValueError)
            pass
        try:
            print (os.stat(path).st_size)
            if os.stat(path).st_size == 0:
                try:
                    urllib.request.urlretrieve(url_alt, path, MyProgressBar())
                except HTTPError:
                    # TODO: Handle error
                    print("ERROR", HTTPError)
                    pass
                except ValueError:
                    print("ERROR", ValueError)
                    pass
        except Exception:
                pass
    return '{}'.format(ontology_id)


def get_descendants_and_similarities(ontology:str):
    ontology_list = ontology.split(':')
    load_ontology(ontology_list[0])    
    url = "/beacon/beacon/db/ontologies/{}.obo".format(ontology_list[0])
    list_of_cousins = []
    list_of_brothers = []
    list_of_uncles = []
    list_of_grandpas = []
    url_alt = "https://www.ebi.ac.uk/efo/EFO.obo"
    try:
        graph = obonet.read_obo(url)
    except Exception:
        graph = obonet.read_obo(url_alt)
    try:
        descendants = networkx.ancestors(graph, ontology)
    except Exception:
        descendants = ''
    descendants=list(descendants)
    print(descendants)
    path = "/beacon/beacon/db/descendants/{}{}.txt".format(ontology_list[0],ontology_list[1])
    with open(path, 'w') as f:
        for item in descendants:
            f.write(item+"\n")
    f.close()
    try:
        tree = [n for n in graph.successors(ontology)]
        for onto in tree:
            predecessors = [n for n in graph.successors(onto)]
            successors = [n for n in graph.predecessors(onto)]
            list_of_brothers.append(successors)
            list_of_grandpas.append(predecessors)
        similarity_high=[]
        similarity_medium=[]
        similarity_low=[]
        for llista in list_of_grandpas:
            for item in llista:
                uncles = [n for n in graph.predecessors(item)]
                list_of_uncles.append(uncles)
                for uncle in uncles:
                    cousins = [n for n in graph.predecessors(uncle)]
                    if ontology not in cousins:
                        list_of_cousins.append(cousins)

        for llista in list_of_brothers:
            for item in llista:
                similarity_high.append(item)
                similarity_medium.append(item)
                similarity_low.append(item)

        for llista in list_of_cousins:
            for item in llista:
                similarity_medium.append(item)
                similarity_low.append(item)
        
        for llista in list_of_uncles:
            for item in llista:
                similarity_low.append(item)

    except Exception:
        similarity_high=[]
        similarity_medium=[]
        similarity_low=[]
    dict={}
    dict[ontology]={}
    dict[ontology]['descendants']=descendants
    dict[ontology]['similarity_high']=similarity_high
    dict[ontology]['similarity_medium']=similarity_medium
    dict[ontology]['similarity_low']=similarity_low
    
    path = "/beacon/beacon/db/similarities/{}{}{}.txt".format(ontology_list[0],ontology_list[1],'high')
    with open(path, 'w') as f:
        for item in similarity_high:
            f.write(item+"\n")
    f.close()
    path = "/beacon/beacon/db/similarities/{}{}{}.txt".format(ontology_list[0],ontology_list[1],'medium')
    with open(path, 'w') as f:
        for item in similarity_medium:
            f.write(item+"\n")
    f.close()
    path = "/beacon/beacon/db/similarities/{}{}{}.txt".format(ontology_list[0],ontology_list[1],'low')
    with open(path, 'w') as f:
        for item in similarity_low:
            f.write(item+"\n")
    f.close()
    
i=0
path_filtering_terms= '/beacon/beacon/db/filtering_terms'

for filename in os.listdir(path_filtering_terms):
    file = os.path.join(path_filtering_terms, filename)
    with open(file, 'r') as f:
        for line in f:
            i +=1
            line = line.replace("\n","")
            get_descendants_and_similarities(line)
            print(i)
    
