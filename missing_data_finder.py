import json
import re

IMDB_IDS_FILE = './imdb-top1000.txt'
DATA_FILE = './movies.json'

movie_ids = []  # All movie IDs
with open(IMDB_IDS_FILE, 'r') as f:
    for id in f:
        id = re.sub(r'\s+', '', id)
        if re.match(r'tt\d+', id):
            movie_ids.append(id)

movie_ids_with_data = []
with open(DATA_FILE, 'r') as data_file:
    movies = json.load(data_file)
    for movie in movies:
        movie_ids_with_data.append(movie['id'])

missing_data_ids = list(set(movie_ids) - set(movie_ids_with_data))
for id in missing_data_ids:
    print(id)

print("We have data for {} movies out of {}".format(len(movie_ids_with_data), len(movie_ids)))
