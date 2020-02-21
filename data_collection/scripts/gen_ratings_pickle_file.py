import pickle
from db.MongoDB import MongoDB

db = MongoDB()
movies = db.movies
LIMIT = 100000

ratings = dict()

total_processed = 0
while True:
    ms = movies.find({}, {'countOfRatings': 1}, limit=LIMIT, skip=total_processed)
    if ms is None:
        break

    for m in ms:
        ratings[m['_id']] = m['countOfRatings']
        total_processed += 1

    if total_processed % LIMIT != 0:
        break

pickle.dump(ratings, open('movie_ratings.p', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
