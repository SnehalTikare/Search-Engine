import math
from bs4 import BeautifulSoup
import numpy as np
from collections import defaultdict
import pickle
import re
import json
from preprocessing import preprocessing,removeStopWords,porterStemmer
import operator
import spacy
from nltk.stem import PorterStemmer

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

def get_result(query):
    original_query = query
    query_tokenized=preprocessing(query)
    query_tokenized=removeStopWords(query_tokenized)
    query_stem=porterStemmer(query_tokenized)
    query_nostop=removeStopWords(query_stem)
    query_tokens=removeWords(query_nostop)
    query_list = [item for sublist in query_tokens for item in sublist]
    #load dictionaries
    url_doc_index = pickle.load(open("IntermediateFiles/url_doc_index", 'rb'))
    doc_index=pickle.load(open("IntermediateFiles/doc_index", 'rb'))
    inverted_index=pickle.load(open("IntermediateFiles/inverted_index", 'rb'))
    weights_doc=pickle.load(open("IntermediateFiles/weights_doc", 'rb'))
    weights_doc_sq=pickle.load(open("IntermediateFiles/weights_doc_sq", 'rb'))
    keyphrases = pickle.load(open("IntermediateFiles/keyphrases", 'rb'))
    stem_original = pickle.load(open("IntermediateFiles/stem_original", 'rb'))
    stem_to_original = pickle.load(open("IntermediateFiles/stem_to_original", 'rb'))
    link_title = pickle.load(open("IntermediateFiles/link_title", 'rb'))
    tf_idf_sorted=[]
    for i in weights_doc.keys():
        tf_idf_sorted.append(list(sorted(weights_doc[i].items(), key = lambda kv:(kv[1], kv[0]),reverse=True)))
    #Calculating tf,idf and weights of each word in every query
    weights_query=calculateWeightsQuery(query_tokens,doc_index,inverted_index)
     #Calculate cosine similarity between document and query
    cosum_query=calculateCosineSim(weights_query,doc_index,weights_doc,weights_doc_sq) 
    #Sort the similarities in descending order for every query
    #cosine_sorted= sorted(cosum_query.items(), key=operator.itemgetter(1))
    cosine_sorted=list(sorted(cosum_query[0].items(), key = lambda kv:(kv[1], kv[0]),reverse=True))
    ranked_documents=pickle.load(open('IntermediateFiles/ranked_documents', 'rb'))
    ranked_documents_networkx=pickle.load(open('IntermediateFiles/ranked_documents_networkx', 'rb'))
    combined_score = {}
    link_doc_number = {}
    top_documents=[]
    for keys in cosine_sorted:
        if url_doc_index.get(keys[0]) in ranked_documents.keys():
            combined_score[url_doc_index.get(keys[0])] =  keys[1]
            #combined_score[url_doc_index.get(keys[0])] =  ranked_documents.get(url_doc_index.get(keys[0])) 
            #combined_score[url_doc_index.get(keys[0])] = 0.75 * keys[1] + 0.25 * ranked_documents.get(url_doc_index.get(keys[0])) 
        else:
            combined_score[url_doc_index.get(keys[0])] = keys[1] 
        link_doc_number[url_doc_index.get(keys[0])] = keys[0]
        top_documents.append(keys[0])
    combined_score= list(sorted(combined_score.items(), key=lambda x:x[1],reverse=True))
    if len(combined_score)<10:
        length = len(combined_score)
    else:
        length=10

    
    top_word_docs=[]
    top_words=set()
    for i in range(0,length):
        doc_number = top_documents[i]
        index = 0
        inner={}
        for words in tf_idf_sorted[doc_number]:
            if  index < 10:
                inner[words[0]]=words[1]
                top_words.add(words[0])
            else:
                break
            index+=1
        top_word_docs.append(inner)

    
    top_N_words={}
    for word in top_words:
        index=0
        while index<length:
            if word in top_word_docs[index].keys():
                if word in top_N_words.keys():
                    top_N_words[word]+=top_word_docs[index].get(word)
                else:
                    top_N_words[word]=top_word_docs[index].get(word)
            index+=1
        
    top_N_words_sorted = list(sorted(top_N_words.items(), key=lambda x:x[1],reverse=True))
    top_N_words_original=[]
    for keys in top_N_words_sorted:
        try:
            top_N_words_original.append(stem_to_original[keys[0]])
        except:
            pass


    #python -m spacy download en_core_web_sm requires downloading this model
    ps = PorterStemmer()

    top_similar_word={}
    nlp = spacy.load('en_core_web_md')  
    query = nlp(' '.join(original_query))
    for token2 in nlp(' '.join(top_N_words_original)):
        similarity = query.similarity(token2)
        print(query.text, token2.text, similarity)
        stemmed_word = ps.stem(token2.text)
        if(similarity > 0.3) and stemmed_word not in query_list:
            top_similar_word[token2.text]=similarity
    
    top_similar_word= list(sorted(top_similar_word.items(), key=lambda x: x[1],reverse=True))
    suggestions=[]
    for pair in top_similar_word:
        suggestions.append(pair[0])

    #combined_score=list(sorted( combined_score[0].items(), key = lambda kv:(kv[1], kv[0]),reverse=True))  
    # print("Using only cosine similarity")
    '''keyphrase_extracted = []
    for index,keys in enumerate(combined_score):
        if index < 2:
            dindex = link_doc_number.get(keys[0])
            phrase = keyphrases.get(dindex)
            for i in range(0,2):
                top_phrase = phrase[i][0]
                p =''
                for word in top_phrase.split():
                    p+=stem_original[dindex][word]+' '
                keyphrase_extracted.append(p)
        else:
            break'''


    '''for i in range(0,10):
        top_ten_links_file.append(url_doc_index.get(cosine_sorted[i][0]))
        print(url_doc_index.get(cosine_sorted[i][0]))'''
    
    
    top_links= []
    title = []
    # print("Using Cosine similarity and pagerank")
    for i,link in enumerate(combined_score):
        top_links.append((combined_score[i][0],link_title.get(combined_score[i][0])))
        title.append(link_title.get(combined_score[i][0]))

    return top_links,suggestions,title

