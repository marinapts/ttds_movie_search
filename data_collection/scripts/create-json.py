"""
This script takes a subset of movies data from a JSONL file (specified by a text file of iMDB IDs) and copies them
to a new JSON file.
"""
import re
import json

IMDB_IDS_FILE = 'imdb-top1000.txt'
JSONL_FILE = 'movies.jsonl'
OUTPUT_JSON_FILE = 'movies-new.json'

ids = []
with open(IMDB_IDS_FILE) as file:
    for id in file:
        id = re.sub(r'\s+', '', id)
        if re.match(r'tt\d+', id):
            ids.append(id)


transferred_movies = []
with open(JSONL_FILE) as file:
    for movie in file:
        movie = json.loads(movie)
        if movie['id'] in ids:
            transferred_movies.append(movie)

with open(OUTPUT_JSON_FILE, 'w') as outfile:
    json.dump(transferred_movies, outfile)

print("{} movies transferred to a new file.".format(len(transferred_movies)))
