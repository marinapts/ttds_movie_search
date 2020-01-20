import json
from collections import defaultdict

DATA_FILE = 'movies.jsonl'
movie_properties = ['id', 'title', 'description', 'categories', 'thumbnail', 'year', 'rating', 'countOfRatings', 'cast', 'plotKeywords']  # no quotes because quotes are saved separately

missing = defaultdict(int)
total = 0

with open('movies.jsonl', 'r') as file:
    for line in file:
        total += 1
        movie = json.loads(line)
        for key in movie_properties:
            if key not in movie:
                missing[key] += 1
                print("{} missing {}".format(movie['id'], key))
            elif key in ['categories', 'cast', 'plotKeywords'] and len(movie[key]) == 0:
                missing[key] += 1
                print("{} missing {}".format(movie['id'], key))


print("Statistics (out of {} movies):".format(total))
for key in movie_properties:
    print("missing {}: {}".format(key, missing[key]))
