import os
import shutil
import json
import re

FOLDER_STRUCTURE_DEPTH = 3

movies = None

def exists_quotes(id, quotes_folder):
    path = quotes_folder
    # Navigate the folder structure
    for i in range(2, 2 + FOLDER_STRUCTURE_DEPTH):
        path = os.path.join(path, id[i])
        if not os.path.exists(path):
            os.mkdir(path)

    # Now we're at the correct folder. Check if file exists
    path = os.path.join(path, "{}.txt".format(id))
    return os.path.exists(path)


def exists_subtitles(id, subtitles_folder):
    path = subtitles_folder
    # Navigate the folder structure
    for i in range(2, 2 + FOLDER_STRUCTURE_DEPTH):
        path = os.path.join(path, id[i])
        if not os.path.exists(path):
            os.mkdir(path)

    # Now we're at the correct folder. Check if file exists
    path = os.path.join(path, "{}.srt".format(id))
    return os.path.exists(path)


def exists_data(id, data_file):
    if not os.path.exists(data_file):
        return False

    global movies
    if movies is None:
        movies = []
        with open(data_file, 'r') as file:
            for line in file:
                movies.append(json.loads(line))

    for movie in movies:
        if movie['id'] == id:
            return True
    return False