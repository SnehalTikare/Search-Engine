'''
Name - Snehal Tikare
NetId - stikar2
Information Retrieval Assignment 3
'''
import math
import networkx as nx
import numpy as np
import json
from functionModule import *
from preprocessing import read_json_files
from collections import defaultdict
from nltk.util import ngrams
from nltk.tokenize import WhitespaceTokenizer
from nltk import pos_tag
from nltk.tokenize import word_tokenize 
from VectorSpaceModel import preprocess_contents
import pickle

#Function to stem the documents
def stem_document(docs):
    stemmer=PorterStemmer()
    stem_document=[]
    for doc in docs:
        stem_current_document=[]
        for line in doc.split("\n"):
            if line:
                phrase = ''
                for word in line.split():
                    phrase+= stemmer.stem(word) +' '
                stem_current_document.append(phrase.strip())
        stem_document.append(stem_current_document)
    return stem_document

#Remove POS tags
def removePOS_Original(documents):
    original_nonpos=[]
    for sen in documents:
        sub=[]
        for words in sen:
            if words.split('_')[0].isalpha():
                sub.append(words.split('_')[0])
        if len(sub)>0:
            original_nonpos.append(sub)
    return original_nonpos
    
def tokenizeOriginal(corpus):
    abstracts =[]
    for doc in corpus:
        token = WhitespaceTokenizer().tokenize(doc)
        abstracts.append(token)
    return abstracts

def tokenize_Candidates(tokenized_corpus):
    split_corpus=[]
    for para in tokenized_corpus:
        split_word=[]
        for word in para:
            split_word.append(word.split('_'))
        split_corpus.append(split_word)
    return split_corpus

def get_candidate(split_corpus):
    pos_tag = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']
    stoplist=set(stopwords.words('english'))
    #Consider words only with the listed POS tags
    untagged_corpus=[]
    for para in split_corpus:
        word_untagged=[]
        for word in para:
            if len(word[0])>2 and word[1] in pos_tag and word[0] not in stoplist and word[0].isalpha():
                word_untagged.append(word[0])
        untagged_corpus.append(word_untagged)
    return untagged_corpus

def createGraph(final_corpus):
     #Create graph for each document
    G_all={}
    for index,corpus in enumerate(final_corpus):
        G_all[index] = nx.Graph()
        G_all[index].add_nodes_from(corpus)
    return G_all

#Get adjacent words for edges
def createGramsForEdges(original_stem,window):
    all_grams=[]
    for doc in original_stem:
        grams=[]
        grams = ngrams(doc,window)
        all_grams.append(grams)
    return all_grams

def add_edge(all_grams,G_all):
    grams_final=[]
    for index,grams in enumerate(all_grams):
        gramscopy=[]
        for gram in grams:
            if G_all[index].has_node(gram[0]):
                for i in range(1,len(gram)):
                    if G_all[index].has_node(gram[i]):
                        G_all[index].add_edge(gram[0],gram[i])
            gramscopy.append(gram)
        grams_final.append(gramscopy)
    return grams_final,G_all

def initiliaze_weights(G_all):
    all_weights={}
    for index in G_all.keys():
        weights={}
        for edge in G_all[index].edges():
            weights[edge]=0
        all_weights[index]=(weights)
    return all_weights

def update_weights(grams_final,all_weights):
    for index,gramscopy in enumerate(grams_final):
        for sen in gramscopy:
            for i in range(1,len(sen)):
                temp=(sen[0],sen[i])
                temp_flip = (sen[i],sen[0])
                if (temp in all_weights[index]):
                    all_weights[index][temp] += 1
                elif (temp_flip in all_weights[index]):
                    all_weights[index][temp_flip] += 1
    return all_weights

def add_edge_weights(all_weights,G_all):
    for index in G_all.keys():
        for keys in all_weights[index].keys():
            G_all[index][keys[0]][keys[1]]['weight'] = all_weights[index][keys]
    return G_all

def initiliaze_scores(G_all):
    all_score={}
    for index in G_all.keys():
        n = G_all[index].number_of_nodes()
        words_score={}
        for node in G_all[index].nodes():
            words_score[node]=1/n
        all_score[index]=words_score
    return all_score

def page_rank(G_all,all_score):
    alpha = 0.85
    for index in G_all.keys():
        pi = 1/G_all[index].number_of_nodes()
        i=0
        while(i<10):
            prev_score = all_score
            for node in G_all[index].nodes():  #Each node in graph 
                summation =0
                for neighbor in list(G_all[index].neighbors(node)):  #Neighbors of that node
                    num = G_all[index].get_edge_data(node,neighbor).get('weight')
                    weights_adjacent=0
                    for word in list(G_all[index].neighbors(neighbor)): #Get sum of weights of out edges of each neighbor(Denominator)
                        weights_adjacent += G_all[index].get_edge_data(neighbor,word).get('weight')
                    #if (weights_adjacent !=0):
                    summation += (num/weights_adjacent) * prev_score[index][neighbor]
                all_score[index][node] = (alpha * summation) + (1 - alpha) * pi
            i+=1
    return all_score

def form_ngrams(abstracts,words_score):
    grams_one = ngrams(abstracts,1)
    grams_two = ngrams(abstracts,2)
    grams_three = ngrams(abstracts,3)
    pos_tag_nouns = ['NN', 'NNS', 'NNP', 'NNPS']
    one_gram=[]
    stemmer=PorterStemmer()
    stoplist=set(stopwords.words('english'))
    stemmed_original = {}
    for word in grams_one:
        phrase = word[0].split('_')
        if (phrase[1]) in pos_tag_nouns and phrase[0] not in stoplist and phrase[0].isalpha() and len(phrase[0])>3:
            stemmed_word = stemmer.stem(word[0].split('_')[0])
            one_gram.append(stemmed_word)
            if stemmed_word not in stemmed_original.keys():
                stemmed_original[stemmed_word] = word[0].split('_')[0]
    
    two_gram = []
    for word in grams_two:
        if len(word) == len(set(word)):
            phrase_2 = word[1].split('_')
            phrase_1 = word[0].split('_')
            if phrase_2[1] in pos_tag_nouns and phrase_2[0] not in stoplist and phrase_2[0].isalpha() and len(phrase_2[0])>2:
                if phrase_1[0] not in stoplist and phrase_1[0].isalpha() and len(phrase_1[0])>3:
                    two_gram.append((stemmer.stem(phrase_1[0]), stemmer.stem(phrase_2[0])))
                    stemmed_phrase1 = stemmer.stem(phrase_1[0])
                    if stemmed_phrase1 not in stemmed_original.keys():
                        stemmed_original[stemmed_phrase1] = phrase_1[0]
                    stemmed_phrase2 = stemmer.stem(phrase_2[0])
                    if stemmed_phrase2 not in stemmed_original.keys():
                        stemmed_original[stemmed_phrase2] = phrase_2[0]

    three_gram = []
    for word in grams_three:
        if len(word) == len(set(word)):
            phrase_3 = word[2].split('_')
            phrase_2 = word[1].split('_')
            phrase_1 = word[0].split('_')
            if phrase_3[1] in pos_tag_nouns and phrase_3[0] not in stoplist and phrase_3[0].isalpha() and len(phrase_3[0])>2 :
                if phrase_2[0] not in stoplist and phrase_2[0].isalpha() and len(phrase_2[0])>3:
                    if phrase_1[0] not in stoplist and phrase_1[0].isalpha() and len(phrase_1[0])>3:
                        three_gram.append((stemmer.stem(phrase_1[0] ), stemmer.stem(phrase_2[0]),stemmer.stem(phrase_3[0])))
                        stemmed_phrase1 = stemmer.stem(phrase_1[0])
                        if stemmed_phrase1 not in stemmed_original.keys():
                            stemmed_original[stemmed_phrase1] = phrase_1[0]
                        stemmed_phrase2 = stemmer.stem(phrase_2[0])
                        if stemmed_phrase2 not in stemmed_original.keys():
                            stemmed_original[stemmed_phrase2] = phrase_2[0]
                        stemmed_phrase3 = stemmer.stem(phrase_3[0])
                        if stemmed_phrase3 not in stemmed_original.keys():
                            stemmed_original[stemmed_phrase3] = phrase_3[0]

    scored_document = {}
    for gram in one_gram:
        if gram in words_score.keys():
            scored_document[gram]=words_score[gram]

    for gram in two_gram:
        sum=0
        key = ''
        for word in gram:
            if word in words_score.keys():
                sum+=words_score[word]
            key+=word+' '
        if key:
            scored_document[key.strip()] = sum

    for gram in three_gram:
        sum=0
        key = ''
        for word in gram:
            if word in words_score.keys():
                sum+=words_score[word]
            key+= word + ' '
        if key:
            scored_document[key.strip()] = sum
    scored_sorted = sorted(scored_document.items(), key=lambda x: x[1],reverse=True)
    return scored_sorted,stemmed_original
    #print(scored_sorted)

def pos_tag_documents(corpus):
    return pos_tag(word_tokenize(corpus))

def concatenate_pos_token(original_docs):
    Documents=[]
    for doc in original_docs:
        sub= []
        for tuples in doc:
            sub.append(tuples[0]+"_"+tuples[1])
        Documents.append(sub)
    return Documents

#Get the file details into list
def main():
    documents=[]
    documents=read_json_files(documents,"json_files")
    pos_tag_docs=[]
    original_docs=[]
    for index, doc in enumerate(documents):
            content = preprocess_contents(doc['contents'])
            if content:
                original_docs.append(content)
                pos_tagged = pos_tag_documents(doc['contents'])
                pos_tag_docs.append(pos_tagged)
    #('chicago uic john', 0.059385453375231774), ('uic campu recreat', 0.05829480202410047), ('chicago uic', 0.05615071761739433), ('at chicago uic', 0.05615071761739433), ('elig uic student', 0.05457839058995667),    
    #print(pos_tag_docs[0])
    Documents = concatenate_pos_token(pos_tag_docs)
    #Tokenize document for choosing candidate words
    untagged_corpus = get_candidate(pos_tag_docs)
    #Get candidate words
    stemmed_corpus = porterStemmer(untagged_corpus)
    #Stem the candidate words
    final_corpus = removeStopWords(stemmed_corpus) 
    original_stem = porterStemmer(original_docs) 
    original_stem = removeStopWords(original_stem)
    #Graph for individual document
    G_all = createGraph(final_corpus)  
    #Stem the Original Document
    Window_size = 2
    all_grams = createGramsForEdges(original_stem,int(Window_size)) 
    #Get the adjacent nodes for edges
    grams_final,G_all = add_edge(all_grams,G_all)
    #Create Edges
    all_weights = initiliaze_weights(G_all) 
    #Initiliaze weights
    all_weights = update_weights(grams_final,all_weights)
    #Update the weights
    G_all = add_edge_weights(all_weights,G_all)
    #Add weights to the edge
    all_score = initiliaze_scores(G_all) 
    #Initialize score of every node in the document
    all_score = page_rank(G_all,all_score) 
    #Call the page rank algorithm

    scored_sorted_doc ={}
    stem_origin_word ={}
    for index, docs in enumerate(Documents):
        scored_sorted_doc[index],stemmed_original = form_ngrams(docs, all_score[index])
        stem_origin_word[index] = stemmed_original
    
    with open("IntermediateFiles/keyphrases", 'wb') as pickle_file:
            pickle.dump(scored_sorted_doc, pickle_file)
    with open("IntermediateFiles/stem_original", 'wb') as pickle_file:
            pickle.dump(stem_origin_word, pickle_file)

    print(scored_sorted_doc[1])
    print(stem_origin_word[0])
    
main()

   
