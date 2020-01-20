import re
import json

ids = []
with open('imdb-top1000.txt') as file:
    for id in file:
        id = re.sub(r'\s+', '', id)
        if re.match(r'tt\d+', id):
            ids.append(id)


transferred_movies = []
with open('movies.jsonl') as file:
    for movie in file:
        movie = json.loads(movie)
        if movie['id'] in ids:
            transferred_movies.append(movie)

with open('movies-new.json', 'w') as outfile:
    json.dump(transferred_movies, outfile)

print("{} movies transferred to a new file.".format(len(transferred_movies)))
