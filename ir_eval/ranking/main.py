import json
import pickle
import numpy as np
import sys
from db.DB import get_db_instance
import math
import time
from ir_eval.utils.score_tracker import ScoreTracker
tracker = ScoreTracker()

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


def term_frequency(term, document_id, relevant_docs):
    """
    Calculates the term frequency in the document.

    Parameters:
        term (string):     a single term
        document_id (int): the document id
    """
    tf = 0
    #if term in words:
        #docs = db.get_index_docs_by_word(term) #inverted_index[term]
        #print(docs)
    if document_id in relevant_docs.keys():
        tf = len(relevant_docs[document_id])
    return tf

def idf(term, docs_for_term, doc_nums):
    """
    Calculates and return the IDF for the term. Returns 0 if DF is 0.

    Parameters:
        term (string): a single term
    """
    df = len(docs_for_term)

    if df == 0:
        return 0
    return math.log10(doc_nums / df)

def tfidf_score_for_doc(term, doc, doc_nums, relevant_docs):
    """
    Returns the list of tfidf scores for the terms and the doc.

    Parameters:
        term (string): a single term
        document_id (int): the document id
    """
    #print('tfidf_score_for_doc')
    result = []
    tf = term_frequency(term, doc, relevant_docs)
    if tf > 0:
        tf = math.log10(tf)
        result = (1 + tf) * idf(term, relevant_docs, doc_nums)
    return result

def tfidf_score(query, doc_nums, db):
    """
    Apply preprocess to the query and calculates the tfidf scores for each document having at least one of the terms.

    Parameters:
        term (string): a single term
    """
    terms = query
    result = dict()
    for term in terms:
        relevant_docs = db.get_index_docs_by_word(term)
        for document in relevant_docs:
            score_doc = tfidf_score_for_doc(term, document, doc_nums, relevant_docs)
            if score_doc > 0:
                if document in result.keys():
                    tracker.add_score(document, score_doc)
                    result[document] += score_doc
                else:
                    result[document] = score_doc
    return sorted(result.keys(), key=lambda kv: kv[1], reverse=True)

def ranked_retrieval(query, db):
    doc_nums = 85000000
    """ This function should be called by app.py to perform the ranked retrieval
    """
    return tfidf_score(query, doc_nums, db)[0:10]

if __name__ == '__main__':
    # @TODO: Get quotes and quote ids
    db = get_db_instance()

    #@TODO: replace this by real number of documents
    doc_nums = 85000000

    t0 = time.time()
    query = ["may", "boy", "girl"]
    result = (tfidf_score(query, doc_nums, db))
    t1 = time.time()
    print(result[0:10])
    print(tracker.get_top(10))
    print(t1-t0)
