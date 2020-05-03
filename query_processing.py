import math
from bs4 import BeautifulSoup
import numpy as np
#from functionModule import *
from collections import defaultdict
import pickle
import re
import json
from preprocessing import *
import operator
from VectorSpaceModel import *

def get_result(query):
    query_tokenized=preprocessing(query)
    query_tokenized=removeStopWords(query_tokenized)
    query_stem=porterStemmer(query_tokenized)
    query_nostop=removeStopWords(query_stem)
    query_tokens=removeWords(query_nostop)

    #load dictionaries
    url_doc_index = pickle.load(open("IntermediateFiles/url_doc_index", 'rb'))
    doc_index=pickle.load(open("IntermediateFiles/doc_index", 'rb'))
    inverted_index=pickle.load(open("IntermediateFiles/inverted_index", 'rb'))
    weights_doc=pickle.load(open("IntermediateFiles/weights_doc", 'rb'))
    weights_doc_sq=pickle.load(open("IntermediateFiles/weights_doc_sq", 'rb'))
    #Calculating tf,idf and weights of each word in every query
    weights_query=calculateWeightsQuery(query_tokens,doc_index,inverted_index)
     #Calculate cosine similarity between document and query
    cosum_query=calculateCosineSim(weights_query,doc_index,weights_doc,weights_doc_sq) 
    #Sort the similarities in descending order for every query
    #cosine_sorted= sorted(cosum_query.items(), key=operator.itemgetter(1))
    cosine_sorted=list(sorted(cosum_query[0].items(), key = lambda kv:(kv[1], kv[0]),reverse=True))
    ranked_documents=pickle.load(open('ranked_documents', 'rb'))
    combined_score = {}
    for keys in cosine_sorted:
        combined_score[url_doc_index.get(keys[0])] = keys[1] + ranked_documents.get(url_doc_index.get(keys[0])) 
    combined_score= sorted(combined_score.items(), key=lambda x:x[1],reverse=True)
    #combined_score=list(sorted( combined_score[0].items(), key = lambda kv:(kv[1], kv[0]),reverse=True))  
    print(cosine_sorted[1][0])
    top_ten_links_file= []
    for i in range(0,10):
        top_ten_links_file.append(url_doc_index.get(cosine_sorted[i][0]))
        print(url_doc_index.get(cosine_sorted[i][0]))
    return top_ten_links_file

