import math
import networkx as nx
import numpy as np
from functionModule import *
from collections import defaultdict
from nltk.util import ngrams
from nltk.tokenize import WhitespaceTokenizer
import pickle

def main():
    print("pagerank")
    crawled_links=pickle.load(open('crawled_links', 'rb'))
    out_links=pickle.load(open('out_links', 'rb'))
    G = nx.Graph()
    


main()