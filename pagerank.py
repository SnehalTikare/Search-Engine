import math
import networkx as nx
import numpy as np
from collections import defaultdict
from nltk.util import ngrams
from nltk.tokenize import WhitespaceTokenizer
import pickle
from preprocessing import *

def initiliaze_scores(G):
    node_score={}
    for node in G.nodes():
        node_score[node]=1/G.number_of_nodes()
    return node_score

def page_rank(G,node_score,origin_outlink):
    i=0
    e=0.15
    n = G.number_of_nodes()
    while(i<50):
        prev_score = node_score
        sum =0 
        for node in G.nodes():  #Each node in graph 
            sum =0 
            for neighbor in list(G.predecessors(node)):  #Neighbors of that node
                if len(list(G.neighbors(neighbor)))>0:
                    sum += prev_score[neighbor] / len(list(G.neighbors(neighbor)))
            node_score[node] = ((1-e) * sum) + e/n       
        i+=1
    return node_score

def pagerank_networkx(G):
    pg_networkx = nx.pagerank(G,alpha=0.15,max_iter=50)
    return pg_networkx

def main():
    '''crawled_links=pickle.load(open('crawled_links', 'rb'))
    out_links=pickle.load(open('out_links', 'rb'))'''
    outlinks=[]
    outlinks=read_json_files(outlinks,"json_files")
    contents=[]
    with open("CrawledFiles/crawled_links.txt","r") as f:
        for line in f:
            contents.append(line.strip())
    f.close()

    G = nx.DiGraph()
    for link in contents:
        G.add_node(link)

    origin_outlink ={}
    for doc in outlinks:
        origin = doc['origin_link']
        out=doc['outlinks']
        origin_outlink[origin] = out
        if G.has_node(origin):
            for link in out:
                if G.has_node(link):
                    G.add_edge(origin,link)
    
    node_score = initiliaze_scores(G)
    node_score = page_rank(G,node_score,origin_outlink)
    node_score_networkx = pagerank_networkx(G)
    with open("IntermediateFiles/ranked_documents", 'wb') as pickle_file:
        pickle.dump(node_score, pickle_file)
    with open("IntermediateFiles/ranked_documents_networkx", 'wb') as pickle_file:
        pickle.dump(node_score_networkx, pickle_file)   
    
#main()