"""
This script finds the ids of movies that we have the data for (in the DATA_FILE) and the ids of movies for which the
data is missing (based on a text file IMDB_IDS_FILE consisting of all wanted movie ids).
"""
import json
import re

IMDB_IDS_FILE = './imdb_at_least_100_ratings.txt'
DATA_FILE = './movies.jsonl'

movie_ids = []  # All movie IDs
with open(IMDB_IDS_FILE, 'r') as f:
    for id in f:
        id = re.sub(r'\s+', '', id)
        if re.match(r'tt\d+', id):
            movie_ids.append(id)

movie_ids_with_data = []
with open(DATA_FILE, 'r') as data_file:
    ext = DATA_FILE.split('.')[-1]
    if ext == 'json':
        movies = json.load(data_file)
        for movie in movies:
            movie_ids_with_data.append(movie['id'])
    elif ext == 'jsonl':
        for line in data_file:
            movie = json.loads(line)
            movie_ids_with_data.append(movie['id'])


missing_data_ids = list(set(movie_ids) - set(movie_ids_with_data))
for id in missing_data_ids:
    print(id)

print("We have data for {} movies out of {}".format(len(movie_ids_with_data), len(movie_ids)))
with open('ids.txt', 'w') as file:
    for id in movie_ids_with_data:
        file.write("{}-{}\n".format(str(int(id.lstrip('t0'))), id))
