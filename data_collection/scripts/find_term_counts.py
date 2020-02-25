"""
This script computes the average processed (stop words removed) sentence length based on the sentences collection.
"""
import pickle
from db.MongoDB import MongoDB
from pymongo.operations import UpdateMany
from collections import defaultdict
import pprint
import csv
from ir_eval.preprocessing import preprocess

START_COUNT = 57600000

mongo = MongoDB()
sentences = mongo.sentences
movies = mongo.movies
LIMIT = 100000


total_counted = START_COUNT
# movie_term_counts = defaultdict(lambda: 0)
movie_term_counts = pickle.load(open('movie_term_counts.p', 'rb'))
movie_id = list(movie_term_counts.keys())[-1]
movie_term_count = movie_term_counts[movie_id]
try:
    while True:
        ss = sentences.find({}, {"sentence": 1, "movie_id": 1, "_id": 0}, skip=total_counted)
        if ss is None:
            break
        for s in ss:
            if s['movie_id'] != movie_id:
                movie_term_counts[movie_id] = movie_term_count
                movie_id = s['movie_id']
                movie_term_count = 0
            terms = set(preprocess(s['sentence']))
            movie_term_count += len(terms)
            total_counted += 1
            if total_counted % 10000 == 0:
                print(f"Count: {total_counted}, Total movies: {len(movie_term_counts)}")
        movie_term_counts[movie_id] = movie_term_count
        if total_counted % LIMIT != 0:
            break
except:
    pass

pickle.dump(dict(movie_term_counts), open(f'movie_term_counts{int(total_counted/100000)}.p', 'wb'))
print("Finished.")
