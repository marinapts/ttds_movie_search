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


def term_frequency(term, document_id, relevant_docs, relevant_movies):
    """
    Calculates the term frequency in the document.

    Parameters:
        term (string):     a single term
        document_id (int): the document id
    """
    tf = 0

    if document_id in relevant_docs.keys():
        tf = len(relevant_movies['movies'][relevant_docs[document_id][0]]['sentences'][relevant_docs[document_id][1]]['pos'])
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

def tfidf_score_for_doc(term, doc, doc_nums, relevant_docs, relevant_movies):
    """
    Returns the list of tfidf scores for the terms and the doc.

    Parameters:
        term (string): a single term
        document_id (int): the document id
    """
    result = []
    tf = term_frequency(term, doc, relevant_docs, relevant_movies)
    if tf > 0:
        tf = math.log10(tf)
        tfidf = (1 + tf) * idf(term, relevant_docs, doc_nums)
    return tfidf

def tfidf_score(query, doc_nums, db):
    """
    Apply preprocess to the query and calculates the tfidf scores for each document having at least one of the terms.

    Parameters:
        term (string): a single term
    """
    terms = query
    for term in terms:
        relevant_movies = db.get_indexed_documents_by_term(term)
        relevant_docs = {}
        for movie in relevant_movies['movies'].keys():
            for doc_id in relevant_movies['movies'][movie]['sentences'].keys():
                relevant_docs[int(doc_id)] = movie
        for document in relevant_docs.keys():
            score_doc = tfidf_score_for_doc(term, document, doc_nums, relevant_docs, relevant_movies)
            if int(score_doc) > 0:
                tracker.add_score(document, score_doc)


def ranked_retrieval(query, db):
    doc_nums = 85000000
    """ This function should be called by app.py to perform the ranked retrieval
    """
    ranking_query_BM25(query, db)
    result_tracker = [item[0] for item in tracker.get_top(100)]
    return result_tracker

def ranking_query_BM25(query, db):
    terms = query
    #query_result_score = dict()
    doc_nums = 85000000
    for term in terms:
        num_splits = db.splits_per_term(term)
        for i in range(0, num_splits):
            relevant_movies = db.get_indexed_documents_by_term(term, i)
            relevant_docs = {}
            for m, movie in enumerate(relevant_movies['movies']):
                movie_id = movie['_id']
                for s, sentence in enumerate(movie['sentences']):
                    quote_id = sentence['_id']
                    relevant_docs[int(quote_id)] = (m, s)
            doc_nums_term = relevant_movies['doc_count']
            for document in relevant_docs.keys():
                term_freq = term_frequency(term, document, relevant_docs, relevant_movies)
                dl = get_dl(term, document, relevant_docs, relevant_movies)
                if dl < 100000:
                    score = score_BM25(doc_nums, doc_nums_term, term_freq, k1=1.2, b=200, dl=dl, avgdl=20)
                else:
                    score = 0
                if score > 0:
                    tracker.add_score(document, int(score))

def score_BM25(doc_nums, doc_nums_term, term_freq, k1, b, dl, avgdl):
    K = compute_K(k1, b, dl, avgdl)
    idf_param = math.log( (doc_nums-doc_nums_term+0.5) / (doc_nums_term+0.5) )
    next_param = ((k1 + 1) * term_freq) / (K + term_freq)
    return float("{0:.4f}".format(next_param * idf_param))


def compute_K(k1, b, dl, avgdl):
    return k1 * ((1-b) + b * (float(dl)/float(avgdl)) )

def get_dl(term, document_id, relevant_docs, relevant_movies):
    return relevant_movies['movies'][relevant_docs[document_id][0]]['sentences'][relevant_docs[document_id][1]]['len']


if __name__ == '__main__':

    db = get_db_instance()

    #@TODO: replace this by real number of documents
    doc_nums = 85000000

    query = ["may", "boy", "girl"]

    ranking_query_BM25(query, db)
    print(tracker.get_top(10))


