import json
import pickle
import numpy as np
import sys
from db.DB import get_db_instance
import math
import time
from ir_eval.utils.score_tracker import ScoreTracker, NaiveScoreTracker
from ir_eval.ranking.phrase_search import phrase_search

MAX_INDEX_SPLITS = 52  # maximum number of different entries in the inverted_index with the same term
TOTAL_NUMBER_OF_SENTENCES = 77584425
batch_size = 20
db = get_db_instance()

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


def ranked_retrieval(query, number_results, search_phrase=False):
    """ This function should be called by app.py to perform the ranked retrieval
    """
    if search_phrase:
        return phrase_search(query, number_results)  # here results is a list of sentence ids, ordered by popularity (descending)
    tracker = ranking_query_BM25(query, batch_size)
    result_ids = [item[0] for item in tracker.get_top(number_results)]
    return result_ids

def ranking_query_BM25(query_params, batch_size=MAX_INDEX_SPLITS):
    tracker = ScoreTracker()
    terms = query_params['query']
    # Prepare advanced search if any filters are provided
    filtered_movies = None
    if len(query_params['movie_title']) > 0 or len(query_params['year']) > 0 or len(query_params['actor']) > 0:
        print('advanced search')
        filtered_movies = db.get_movie_ids_advanced_search(query_params)

    #query_result_score = dict()
    doc_nums = TOTAL_NUMBER_OF_SENTENCES
    for term in terms:
        for i in range(0, MAX_INDEX_SPLITS, batch_size):
            list_of_splitted = db.get_indexed_documents_by_term(term, i, batch_size)
            # process_start = time.time()
            for relevant_movies in list_of_splitted:
                # print("time for processing an index entry: {} s".format(time.time() - process_start))
                # process_start = time.time()
                doc_nums_term = relevant_movies['doc_count']
                for m, movie in enumerate(relevant_movies['movies']):
                    movie_id = movie['_id']
                    if filtered_movies is None or movie_id in filtered_movies:  # advanced search if filtered_movies is initialised
                        for s, sentence in enumerate(movie['sentences']):
                            quote_id = int(sentence['_id'])
                            term_freq = len(sentence['pos'])
                            dl = sentence['len']
                            score = score_BM25(doc_nums, doc_nums_term, term_freq, k1=1.2, b=200, dl=dl, avgdl=20) if dl < 100000 else 0
                            if score > 0:
                                tracker.add_score(quote_id, score)
    return tracker


def score_BM25(doc_nums, doc_nums_term, term_freq, k1, b, dl, avgdl):
    K = compute_K(k1, b, dl, avgdl)
    idf_param = math.log( (doc_nums-doc_nums_term+0.5) / (doc_nums_term+0.5) )
    next_param = ((k1 + 1) * term_freq) / (K + term_freq)
    return float("{0:.4f}".format(next_param * idf_param))


def compute_K(k1, b, dl, avgdl):
    return k1 * ((1-b) + b * (float(dl)/float(avgdl)) )


if __name__ == '__main__':

    db = get_db_instance()
    batch_size = 50

    start = time.time()
    query_params = {'query': ["father"]} #, "boy", "girl"]}
    query_params['movie_title'] = ''
    query_params['year'] = ''
    query_params['actor'] = ''

    tracker = ranking_query_BM25(query_params, batch_size)
    end = time.time()
    print(end-start)

    query_params = {"year": "2000-2001"}
    query_params['query'] = ["may"]
    query_params['movie_title'] = ''
    query_params['actor'] = ''
    start = time.time()
    tracker = ranking_query_BM25(query_params, batch_size)
    end = time.time()
    print(end-start)
    print(tracker.get_top(10))


