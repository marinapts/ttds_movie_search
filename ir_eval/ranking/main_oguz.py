import json
import pickle
import numpy as np
import sys
sys.path.insert(1, '/Users/leonie/Documents/MDS/TTDS/movie_search/api/')
from db.DB import get_db_instance
import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
#stop_words = set(stopwords.words('english'))
import math
import time

def json_load(path):
    """ It loads and returns a json data in dictionary structure.
    Arguments:
        path {string} -- the path of the json data
    Returns:
        dictionary -- the dictionary created from the json data.
    """
    return json.load(open(path))


def load_file_binary(file_name):
    with open(file_name + '.pickle', 'rb') as f:
        return pickle.load(f)

def get_documents_for_term(term, words, docs_for_term):
    """
    Returns a document number list for the documents containing given document.

    Parameters:
        term (string): a single term
    """
    result = list()
    if term in words:
        result = docs_for_term
        #result = db.get_index_docs_by_word(term) #list(inverted_index[term])
    return result

def document_frequency(term, words, docs_for_term):
    """
    Returns the document frequency for the term.

    Parameters:
        term (string): a single term
    """
    return len(get_documents_for_term(term, words, docs_for_term))

def term_frequency(term, document_id, words, docs_for_term):
    """
    Calculates the term frequency in the document.

    Parameters:
        term (string):     a single term
        document_id (int): the document id
    """
    tf = 0
    if term in words:
        #docs = db.get_index_docs_by_word(term) #inverted_index[term]
        #print(docs)
        if document_id in docs_for_term.keys():
            tf = len(docs_for_term[document_id])
    return tf

def idf(term, doc_nums, words, docs_for_term):
    """
    Calculates and return the IDF for the term. Returns 0 if DF is 0.

    Parameters:
        term (string): a single term
    """
    df = document_frequency(term, words, docs_for_term)
    if df == 0:
        return 0
    return math.log10(len(doc_nums) / df)

def tfidf_score_for_doc(terms, doc, doc_nums, words):
    """
    Returns the list of tfidf scores for the terms and the doc.

    Parameters:
        term (string): a single term
        document_id (int): the document id
    """
    #print('tfidf_score_for_doc')
    result = []
    for term in terms:
        docs_for_term = db.get_index_docs_by_word(term) #inverted_index[term]
        tf = term_frequency(term, doc, words, docs_for_term)
        if tf > 0:
            print('tf>0')
            tf = math.log10(tf)
            result.append((1 + tf) * idf(term, doc_nums, words, docs_for_term))
    return result

def tfidf_score(query, doc_nums, words):
    """
    Apply preprocess to the query and calculates the tfidf scores for each document having at least one of the terms.

    Parameters:
        term (string): a single term
    """
    print('tfidf_score')
    terms = query
    result = dict()
    for document in doc_nums:
        score = sum(tfidf_score_for_doc(terms, document, doc_nums, words))
        if score > 0:
            result[document] = score
    return sorted(result.items(), key=lambda kv: kv[1], reverse=True)


def get_doc_nums(inverted_index):
    doc_nums = []
    for word in inverted_index.keys():
       doc_nums.extend(list(inverted_index[word].keys()))
    print(len(doc_nums))
    return doc_nums

if __name__ == '__main__':
    #inverted_index = json_load('inverted_index_files/inverted_index.json')
    with open('inverted_index_small.pickle', 'rb') as handle:
        inverted_index = pickle.load(handle)

    # @TODO: Get quotes and quote ids
    db = get_db_instance()

    #@TODO: Get doc_nums from database
    t0 = time.time()
    documents_word = db.get_index_docs_by_word('may')
    t1 = time.time()
    print(t1-t0)

    #print(type(documents_word[0]))

    #Just for now: get doc_nums from inverted_index
    #doc_nums = db.get_all_quote_ids()

    doc_nums = get_doc_nums(inverted_index)
    doc_nums = doc_nums[0:100]

    words = db.get_all_words()


    # doc_nums = db.get_all_quote_ids() # A list of all the document numbers
    # print('got docnums')
    # doc_nums_list = []
    # for i, element in enumerate(doc_nums):
    #     doc_nums_list.append(list(doc_nums[i].values()))
    # doc_nums = doc_nums_list
    # print(doc_nums[0])


    #Try Oguz:
    t0 = time.time()
    print('start query')
    query = ["may"] #, "boy", "girl"]
    result = (tfidf_score(query, doc_nums, words))
    print(result)
    t1 = time.time()
    print(t1-t0)