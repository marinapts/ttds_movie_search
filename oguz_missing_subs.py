import json
import re
import csv
import io

# Oguz request: given a list of iMDB IDs with missing subtitles, find the movie data:
# IMDB_IDS_FILE = './missing.txt'
# DATA_FILE = './movies.jsonl'
#
# movie_ids = []  # All movie IDs
# with open(IMDB_IDS_FILE, 'r') as f:
#     for id in f:
#         id = re.sub(r'\s+', '', id)
#         if re.match(r'tt\d+', id):
#             movie_ids.append(id)
#
#
# found_movies = []
# with open(DATA_FILE, 'r') as data_file:
#     for line in data_file:
#         movie = json.loads(line)
#         if movie['id'] in movie_ids:
#             found_movies.append(movie)
#
# with open('missing.csv', 'w', newline='') as csvfile:
#     fieldnames = ['id', 'title', 'rating', 'numOfRatings']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     writer.writeheader()
#     for movie in found_movies:
#         writer.writerow({'id': movie['id'], 'title': movie['title'], 'rating': movie['rating'], 'numOfRatings': movie['countOfRatings']})


SUB_IDS_FILE = './owned_ids.txt'
DATA_FILE = './movies.jsonl'

owned_sub_ids = set()  # IDs of movies we have subs for
with open(SUB_IDS_FILE, 'r') as f:
    for id in f:
        id = re.sub(r'\s+', '', id)
        if re.match(r'tt\d+', id):
            owned_sub_ids.add(id)

print("{} sub ids owned".format(len(owned_sub_ids)))


missing_movies = []
with open(DATA_FILE, 'r') as data_file:
    for line in data_file:
        movie = json.loads(line)
        if movie['id'] not in owned_sub_ids:
            missing_movies.append(movie)

print("{} subs missing".format(len(missing_movies)))

with io.open('missing.csv', mode='w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['id', 'title', 'rating', 'numOfRatings']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for movie in missing_movies:
        writer.writerow({'id': movie['id'], 'title': movie['title'], 'rating': movie['rating'], 'numOfRatings': movie['countOfRatings']})

