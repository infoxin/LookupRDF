'''
Created on Jul 12, 2020

@author: XHG3
'''
import redis 
from ConnectRedis import r
import pandas as pd
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import Namespace, RDFS, FOAF, RDF,XSD
import pyld
import rdflib
import os

import logging
from sklearn.feature_extraction import stop_words
logging.basicConfig(level= logging.INFO)
logger = logging.getLogger(__name__)

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

stopWords = set(stopwords.words(['english','french']))
# for w in ['!',',','.','?',':','(',')']:
#     stopWords.add(w)
print(stopWords)

# list_triples = []
# list_triples = list( graph.triples((None, RDFS.label, None)) )
# list_triples.extend(graph.triples((None, RDFS.comment, None)))
# list_triples.extend(graph.triples((None, URIRef('http://schema.org/description'), None)))
# list_triples.extend(graph.triples((None, URIRef('http://www.w3.org/2004/02/skos/core#altLabel'), None)))   


predicates = [RDFS.label, URIRef('http://schema.org/description'), URIRef('http://www.w3.org/2004/02/skos/core#altLabel')]

def extractTriples(graph, predicates):
    number_predicate = len(predicates)
    list_triples = []
    list_triples_en = []
    for predicate in predicates:
        list_triples.extend(graph.triples((None, predicate, None)))
#     print('number of triples:',len(list_triples))
#     filter english entity only
    for (s,p,o) in list_triples:
        if(o.language =='en'):
            list_triples_en.append((s,p,o))
#     print('number of english triples:',len(list_triples_en))
    return list_triples_en


def preprocess(doc):
    # tokenize sentences
#     print(doc)
    sentences = nltk.sent_tokenize(doc)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
# tag sentences and use nltk's Named Entity Chunker
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    ne_chunked_sents = [nltk.ne_chunk(tagged) for tagged in tagged_sentences]
# extract all named entities
    named_entities = []
    for ne_tagged_sentence in ne_chunked_sents:
        for tagged_tree in ne_tagged_sentence:
       # extract only chunks having NE labels
            if hasattr(tagged_tree, 'label'):
                entity_name = ' '.join(c[0] for c in tagged_tree.leaves()) #get NE name
                entity_type = tagged_tree.label() # get NE category
                named_entities.append((entity_name, entity_type))
           # get unique named entities
                named_entities = list(set(named_entities))
#     print(named_entities)
#     logger.info('number of entities:'+str(len(named_entities)))
    return named_entities

def indexTriples(list_triples):
    for (s,p,o) in list_triples:
#         print(o, p, s)
        r.lpush(o, s)
        named_entities = preprocess(o)
        for entity in named_entities: 
#             print(entity)
            r.lpush(entity[0], s)
    
def get_files(file_path):
    files_list = []
    for root, dirs, files in os.walk(file_path):
        for name in files:
#             print(os.path.join(root,name))
            files_list.append(os.path.join(root,name))
    return files_list

if __name__ == '__main__':
    
    keys = r.keys()
#     if keys:
#         r.delete(*keys)
    data_path = 'data/taxoWiki_depth_3'
    logger.info('loading graph')

#     data_path = 'E:/Data/taxo.ttl'
    files_list = get_files(data_path)
    data_format = 'ttl'
#     print(files_list)
    for file in files_list:
        print(file)
        graph = Graph()
        graph.parse(file, format= data_format)
#         print('graph size:',len(graph))
        list_triples_en = extractTriples(graph, predicates)
        indexTriples(list_triples_en)
        print(r.dbsize())
        
   
            
    print(r.dbsize())
#     print(r.keys())

    
#  # store named entities in a data frame
# entity_frame = pd.DataFrame(named_entities, columns=['Entity Name', 'Entity Type'])
# # display results
# print(entity_frame)



# ex = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'
# sent = preprocess(ex)
# print(sent)