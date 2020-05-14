## Information-retrieval
Name- Snehal Tikare
NetId- stikar2
Filename :  searchengine.py, run_model.py, crawler.py

The given folder has all the files.Please navigate to the folder or open the folder in a IDE
and run searchengine.py. 
Files consists of relative path and no absolute path.So it should run if all files are in same folder

__Environment:__ <br />
Python version: Python 3 and above <br />

__Libraries :__ <br />
Install the below libraries<br />
Commands may change based on the system used(Windows, Mac, Linux) check accordingly
- pip install -U nltk <br />
- sudo python -m nltk.downloader all <br />
- pip install networkx
- pip install spacy
- pip install pickle
- python -m spacy download en_core_web_sm 
- pip install beautifulsoup4
- pip install scrapy

__Note: some of the functionalities used in the program are compatible with only python 3 and above.__<br />
__Please use python 3 and above to run the program__<br />

__Instructions to run the Search Engine GUI:__<br />

Please note that due to use of spacy library for finding keywords, it takes time for the GUI to display result.

1. Steps to run the file using command line
		1) Go to the path where folder 'websearch' is stored
   		2) Type 'Python3 searchengine.py' <br />
Once the command prompt/terminal is open <br />
Type ‘python’ to check the version of python installed<br />

2. Using any IDE
	a) Open the IDE, file -> open the folder where the given folder is saved<br />
	b) Open searchengine.py, right click-> choose ‘Run python file in terminal’<br />

__Instructions to run the crawler:__<br />

1. Navigate to the file crawler.py ( websearch -> websearch -> crawler.py)
	a) Open the terminal and type "scrapy crawl uic_crawler"
	  (To change the seed site, change the url in start_url in file crawler.py)
	  (To change number of sites to be crawled, go to settings.py in websearch and change the line CLOSESPIDER_PAGECOUNT = xxxx where xxxx is desired number of sites to br crawled)

	b)After the crawler finishes execution, run the run_model.py file to update Vector Space model and Page rank.

__Functionalities of each module of the file preprocessing.py__<br />
1) def get_files<br />
Reads all the files from the specified path and returns a list<br />
Argument: Empty list<br />
Return list containing information from all the files<br /> 

2) def preprocessing(corpus):<br />
Function to preprocess the data<br />
Argument:list of strings<br />
Return tokenized lists <br />

3) def numberOfWords(tokenized):<br />
Function that returns total number of tokens in a list<br />
Argument tokenized list<br />
Returns the number of words in list<br />

4) def getMostCommon(tokenized,i):<br />
Function that return the top K frequent words in a list<br />
Arguments: tokenized list, i: K (top k frequent word)<br />

5) def numberWordPercent(tokenized,per):<br />
Function that returns the number of words accounting for x% of total words<br />
Argument: tokenized list, percentage<br />

6) def getStopWords(mostcommon):<br />
Function that returns the list of stop words in top K frequent words<br />
Arguments: list of top frequent words<br />

7) def stopWordList():<br />
Function that returns list of stopwords<br />

8) def removeStopWords(tokenized):<br />
Function to remove stopwords from the given tokens<br />
Argument : tokenized list<br />

9) def porterStemmer(token_nostop):<br />
Function to stem the list of tokens using porterStemmer of nltk library<br />
Argument: tokenized list containing no stop words <br />

__Functionalities of each module of the file VectorSpaceModel.py__<br />

This is the main file containing the main function.
functionModule.py is imported in this function

1)def getTitleAndText(corpus):
Function to get the text between title and text tags and remove SGML tags
Library used: beautifulSoup

2)def removeWords(tokens):
Function to remove words of length less than 3 from the list of the tokens

3)def invertedIndex(tokens):
Create the inverted index of the tokens in each of the documents
Returns a dictionary with tokens as key and another dictionary which contains term frequency in each documnent as value

4)def calculateWeightsDoc(tokens,mainDict):
Calculate the weights of each word in every documents
First step is to calculate the Term frequency of each word in the document,Next calculate Inverse document frequency.
Lastly calculate weight using formula tf * idf

5)def calculateWeightsQuery(query_tokens,tokens,mainDict):
Calculate the weights of each word in every query
First step is to calculate the Term frequency of each word in the query,Next calculate Inverse document frequency.
Lastly calculate weight using formula tf * idf

6)def calculateCosineSim(weights_query,tokens,weights_doc,weights_doc_sq):
Calculate the cosine similarity between each query and the document


__Functionalities of each module of the file Keyphrase.py__<br />

1)def stem_document(docs):
Stem the documents extracted from the gold folder.

2)def removePOS_Original(documents):
Remove the POS tags from the documents in the abstract folder and keep only the words.

3)def tokenizeOriginal(corpus), def tokenize_Candidates(tokenized_corpus)::
Tokenize the original documents as well the documents for choosing the candidate words

4)def get_candidate(split_corpus):
Consider words ending tags 'NN', 'NNS', 'NNP', 'NNPS', 'JJ' as candidate for creating the node of the graph.

5)def createGraph(final_corpus):
Use Graph from networkx's library to create the graph with desired words as nodes from previous step.
One graph is created for every document.

6)def createGramsForEdges(original_stem,window):
Use the ngram function from nltk library to choose adjacent words from the original document for creating edges of the graph

7)def add_edge(all_grams,G_all):
Add edge between nodes using the result from the above step.

8)def initiliaze_weights(G_all):
Initiliaze weights of the edges of every graph as zero

9)def update_weights(grams_final,all_weights),def add_edge_weights(all_weights,G_all)::
Use the original document to calculate and update the edge weight according to the adjacency rule

10)def initiliaze_scores(G_all):
Initialize the scores of all the candidate words as zero

11)def page_rank(G_all,all_score):
Use the page rank algorithm to update the scores of the nodes.
Iteration = 10
alpha = 0.85

12)def form_ngrams(abstracts,words_score):
Form phrases from unigrams, bigrams, trigrams adding the individual scores of every word
Unigrams, bigrams and trigrams end with a noun












