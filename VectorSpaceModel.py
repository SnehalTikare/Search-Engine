import math
from bs4 import BeautifulSoup
import numpy as np
from collections import defaultdict
import pickle
import re
import json
from preprocessing import *
import operator

#Function to remove words of length less than 3
def removeWords(tokens):
    final=[]
    for line in tokens:
        token=[]
        for words in line:
            if(len(words)<3):
                continue
            token.append(words)
        final.append(token)
    return final

#Create the inverted index of the tokens in each of the documents
def invertedIndex(tokens):
    mainDict={} #Hash table to store toekns as key and another dictionary as value
    i=0
    for line in tokens:
        for word in line:
            subDict={}#Dictionary consisting of documents as key and term frequency of token in that document
            if word not in mainDict:
                subDict[i]=1
                mainDict[word]=subDict
            else:
                temp=mainDict.get(word)
                if i not in temp.keys():
                    temp[i]=1
                else:
                    temp[i]+=1
        i=i+1
    return mainDict

#Calculate most frequent in each document
def max_word_document(tokens):
    maxFreq={}
    for index,docs in enumerate(tokens):
        max=0
        for word in docs:
            if (docs.count(word) >= max):
                max=docs.count(word) 
        maxFreq[index] = max
    return maxFreq


#Calculate the weights of each word in every documents
def calculateWeightsDoc(tokens,mainDict,maxFreq):
    weights_doc={}
    weights_doc_sq={}
    i=0
    for docs in tokens:
        no_terms_doc=len(docs)
        weights_word={}
        squared_weights=0
        for word in set(docs):
            in_docs=mainDict.get(word)
            idf=math.log2(len(tokens)/len(in_docs)) #Calculate the inverted document frequency
            #tf=(in_docs.get(i))/no_terms_doc #Calculate the term frequency
            tf=(in_docs.get(i))/maxFreq.get(i)
            weights_word[word]=tf * idf #Calculate the weights
            squared_weights+=math.pow((tf*idf),2)
        weights_doc[i]=weights_word
        weights_doc_sq[i]=squared_weights #Squared weights
        i+=1
    return weights_doc,weights_doc_sq

#Calculate the weights of each word in every query
def calculateWeightsQuery(query_tokens,tokens,mainDict):
    weights_query={}
    i=0
    for quer in query_tokens:
        weights_qtokens={}
        for word in quer:
            if word in mainDict.keys():
                tf=(quer.count(word))/len(quer) #Calculate the inverted document frequency
                idf=math.log2(len(tokens)/len(mainDict[word])) #Calculate the term frequency
                weights_qtokens[word]=tf * idf
        weights_query[i]=weights_qtokens
        i+=1
    return weights_query

#Calculate the cosine similarity between each query and the document
def calculateCosineSim(weights_query,tokens,weights_doc,weights_doc_sq):
    i=0
    j=0
    cosum_query={}
    for quer in weights_query:
        i=0
        cosum_docs={}
        for docs in tokens:
            num=0
            #consider words present in both query and documents
            if not set(weights_query[quer].keys()).isdisjoint(set(docs)):
                #Iterate through list of words present in query and documents
                for word in (set(weights_query[quer].keys()).intersection(set(docs))): 
                    num+=(weights_query[quer].get(word))* (weights_doc[i].get(word))
                deno=math.sqrt(weights_doc_sq[i])
                cosum=num/deno
                cosum_docs[i]=cosum
            i+=1
        cosum_query[j]=cosum_docs
        j+=1
    return cosum_query

def preprocess_contents(corpus,stem_to_original):
    ps = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    corpus=corpus.lower().strip()#convert the the words to lower case
    corpus_split = corpus.split()
    processed =[]
    for words in corpus_split:
        words = words.translate(str.maketrans('', '', string.punctuation))
        if words not in stop_words:
            original_word = words
            words = ps.stem(words)
            stem_to_original[words] = original_word
            if words not in stop_words and len(words)>2 and words.isalpha():
                processed.append(words)
    return processed,stem_to_original

def main():
    corpus=[]
    corpus=read_json_files(corpus,"json_files")
    url_doc_index={}
    doc_index=[]
    url_doc={}
    stem_to_original={}
    link_title={}
    for index, doc in enumerate(corpus):
        content,stem_to_original = preprocess_contents(doc['contents'],stem_to_original)
        doc_index.append(content)
        url_doc_index[index] = doc['origin_link']
        link_title[doc['origin_link']] = doc['title']
        url_doc[doc['origin_link']]=content
    #For calculating TF-IDF of terms wrt the documents
    inverted_index = invertedIndex(doc_index)
    maxFreq = max_word_document(inverted_index)
    #Calculating tf,idf and weights of each word in every document
    weights_doc,weights_doc_sq=calculateWeightsDoc(doc_index,inverted_index,maxFreq)
    with open("IntermediateFiles/url_doc_index", 'wb') as pickle_file:
            pickle.dump(url_doc_index, pickle_file)
    with open("IntermediateFiles/inverted_index", 'wb') as pickle_file:
            pickle.dump(inverted_index, pickle_file)
    with open("IntermediateFiles/doc_index", 'wb') as pickle_file:
            pickle.dump(doc_index, pickle_file)
    with open("IntermediateFiles/weights_doc", 'wb') as pickle_file:
            pickle.dump(weights_doc, pickle_file)
    with open("IntermediateFiles/weights_doc_sq", 'wb') as pickle_file:
            pickle.dump(weights_doc_sq, pickle_file)
    with open("IntermediateFiles/stem_to_original", 'wb') as pickle_file:
            pickle.dump(stem_to_original, pickle_file)
    with open("IntermediateFiles/link_title", 'wb') as pickle_file:
            pickle.dump(link_title, pickle_file)

#main()
