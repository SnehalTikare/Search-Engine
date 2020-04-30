'''
Name - Snehal Tikare
NetId - stikar2
Information Retrieval Assignment 2
'''


import math
from bs4 import BeautifulSoup
import numpy as np
from functionModule import *
from collections import defaultdict
import pickle
import re

#Function to get the text between title and text tags
def getTitleAndText(corpus):
    text=[]
    for x in corpus:
        soup = BeautifulSoup(x, features='html.parser')
        text.append(soup.find('title').getText()+soup.find('text').getText())
    return text

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
    i=1
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

#Calculate the weights of each word in every documents
def calculateWeightsDoc(tokens,mainDict):
    weights_doc={}
    weights_doc_sq={}
    i=1
    for docs in tokens:
        no_terms_doc=len(docs)
        weights_word={}
        squared_weights=0
        for word in set(docs):
            in_docs=mainDict.get(word)
            idf=math.log2(len(tokens)/len(in_docs)) #Calculate the inverted document frequency
            tf=(in_docs.get(i))/no_terms_doc #Calculate the term frequency
            weights_word[word]=tf * idf #Calculate the weights
            squared_weights+=math.pow((tf*idf),2)
        weights_doc[i]=weights_word
        weights_doc_sq[i]=squared_weights #Squared weights
        i+=1
    return weights_doc,weights_doc_sq

#Calculate the weights of each word in every query
def calculateWeightsQuery(query_tokens,tokens,mainDict):
    weights_query={}
    i=1
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
    i=1
    j=1
    cosum_query={}
    for quer in weights_query:
        i=1
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


#Function to calculate precision and recall of the queries and documents
def precisionAndRecall(query,ranking,relevance,cosine_sim):
    top=[]
    for i in range(0,ranking):
        top.append(cosine_sim[query-1][i][0])
    
    relevantfirst=[]
    for i in range(len(relevance)):
        if int(relevance[i][0])==query:
            relevantfirst.append(int(relevance[i][1]))
    #Precision = Number of relevant documents retrieved /Total number of documents retrieved
    precision=len(set(top) & set(relevantfirst))/len(top)
    #Recall = Number of relevant documents retrieved/Total number of relevant documents
    recall=len(set(top) & set(relevantfirst))/len(relevantfirst)
    return precision,recall

#Get the file details into list
def main():
    corpus=[]
    #path1=input("Enter the path where the documents are stored:") or "cranfieldDocs"
    corpus=get_files(corpus,"files")
    #print(corpus[0])
    tokenized=preprocessing(corpus)
    tokenized=removeStopWords(tokenized)#Added a condition to check if len(word) is greater than 2
    #Perform stemming of the tokenized words from the documents
    token_stem=porterStemmer(tokenized)
    #Remove stopwords after stemming 
    token_nostop=removeStopWords(token_stem)
    #Remove words of length than 3
    tokens=removeWords(token_nostop)
    #print(tokens[0])
    #Create Inverted Index of the documents
    mainDict=invertedIndex(tokens)
    #Calculating tf,idf and weights of each word in every document
    weights_doc,weights_doc_sq=calculateWeightsDoc(tokens,mainDict)
    #Read Query text files
    #query_path=input("Enter the path where the queries are stored:") or 'queries.txt'
    query=[]
    with open('queries.txt', 'r') as f:
        for line in f:
            query.append(line)
    query_tokenized=preprocessing(query)
    query_tokenized=removeStopWords(query_tokenized)
    query_stem=porterStemmer(query_tokenized)
    query_nostop=removeStopWords(query_stem)
    query_tokens=removeWords(query_nostop)
    #Calculating tf,idf and weights of each word in every query
    weights_query=calculateWeightsQuery(query_tokens,tokens,mainDict)
    #Calculate cosine similarity between document and query
    cosum_query=calculateCosineSim(weights_query,tokens,weights_doc,weights_doc_sq) 
    #Sort the similarities in descending order for every query
    cosine_sim=list(sorted(cosum_query[1].items(), key = lambda kv:(kv[1], kv[0]),reverse=True))
    print(cosine_sim[2][0])
    top_ten_links_file= []
    for i in range(0,10):
        top_ten_links_file.append(cosine_sim[i][0])
    file_links=pickle.load(open('files_link', 'rb'))
    top_ten_links=[]
    for num in top_ten_links_file:
        for key in file_links.keys():
            file_num = (re.findall('\d+', key ))
            if str(num) in file_num:
                top_ten_links.append(file_links.get(key))
    for link in top_ten_links:
        print(link + "\n")

            


    #print(file_links)
    '''
    text=getTitleAndText(corpus) #Get text from title and text tags

    #Perform preprocessing of the documents and queries and tokenize them
    tokenized=preprocessing(text)
    query_tokenized=preprocessing(query)
    
    #Remove stop words from the documents and queries
    tokenized=removeStopWords(tokenized)
    query_tokenized=removeStopWords(query_tokenized)
    
    #Perform stemming of the tokenized words from the documents and queries
    token_stem=porterStemmer(tokenized)
    query_stem=porterStemmer(query_tokenized)

    #Remove stopwords after stemming 
    token_nostop=removeStopWords(token_stem)
    query_nostop=removeStopWords(query_stem)

    #Remove words of length than 3
    tokens=removeWords(token_nostop)
    query_tokens=removeWords(query_nostop)

    #Create Inverted Index of the documents
    mainDict=invertedIndex(tokens)
  
    #Calculating tf,idf and weights of each word in every document
    weights_doc,weights_doc_sq=calculateWeightsDoc(tokens,mainDict)
   
    #Calculating tf,idf and weights of each word in every query
    weights_query=calculateWeightsQuery(query_tokens,tokens,mainDict)

    #Calculate cosine similarity between document and query
    cosum_query=calculateCosineSim(weights_query,tokens,weights_doc,weights_doc_sq)    

   #Sort the similarities in descending order for every query
    cosine_sim=[]
    for i in range(1,11):
        cosine_sim.append(list(sorted(cosum_query[i].items(), key = lambda kv:(kv[1], kv[0]),reverse=True)))

    #Read the relevance.txt file
    relevance=[]
    with open('relevance.txt', 'r') as f:
        for line in f:
            relevance.append(line.split())

    #Print the average precision and recall of each query against range of top ranked documents
    print('\nEvaluating your queries')
    for i in (10,50,100,500):
        print('Top '+ str(i) +' documents in the rank list')
        sumPr=0
        sumRe=0
        for j in range(1,11):
            precision,recall=precisionAndRecall(j,i,relevance,cosine_sim)  #Get the precision and recall
            sumPr+=precision
            sumRe+=recall
            print('Query: '+ str(j)+ " "+ '\tPr: '+ str(precision) + '\t\tRe: '+ str(recall))
        print('Avg precision: ' + str(sumPr/j))
        print('Avg recall: ' + str(sumRe/j))'''
        
    
main()
