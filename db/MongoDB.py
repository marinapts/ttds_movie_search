from typing import List
from flask_pymongo import PyMongo
from pymongo import MongoClient
from db.DBInterface import DBInterface
import gridfs
import json
import re
from operator import itemgetter


class MongoDB(DBInterface):

    BULK_WRITE_LIMIT = 1000

    def __init__(self):
        super().__init__()
        client = MongoClient('167.71.139.222', 27017, username='admin', password='iamyourfather')
        self.ttds = client.ttds
        self.sentences = self.ttds.sentences
        self.inverted_index = self.ttds.inverted_index
        self.movies = self.ttds.movies
        self.sentences.create_index('_id')
        self.inverted_index.create_index('_id')
        self.movies.create_index('_id')
        self.inverted_index_gridfs = gridfs.GridFS(self.ttds)


    def get_quotes_by_list_of_quote_ids(self, ids: List[int]):
        # Given a list of quote ids, return a list of quote dictionaries
        quote_list = list(self.sentences.find({"_id": {"$in": ids}}))
        return quote_list

    def get_quotes_by_movie_id(self, movie_id: str):
        # Given a movie id, returns a list of all sentences in that movie
        quote_list = list(self.sentences.find({"movie_id": movie_id}))
        return quote_list

    def get_movies_by_list_of_ids(self, ids: List[str]):
        # Given a list of movie ids, return a list of movie dictionaries
        movie_list = list(self.movies.find({"_id": {"$in": ids}}))
        return movie_list

    def populate_movies_data(self, file_path: str, clear: bool):
        # Given a file with movies data, populate the database with those movies.
        # File can be either .json or .jsonl
        # clear flag specifies whether all contents of the database should be cleared before populating.

        if clear:  # clear the movies collection before populating
            self.movies.delete_many({})

        movies_list = list()

        with open(file_path, 'r') as file:
            ext = file_path.split('.')[-1]
            if ext == 'json':  # JSON format - the whole file is a JSON list of movies
                movies = json.load(file)
                for movie in movies:
                    movies_list.append(self._process_imdb_movie(movie))
                self.movies.insert_many(movies_list, ordered=False)
            elif ext == 'jsonl':  # JSON Lines format - each line is a JSON object
                for line in file:
                    movie = json.loads(line)
                    movies_list.append(self._process_imdb_movie(movie))
                    if len(movies_list) >= self.BULK_WRITE_LIMIT:  # flush the movies from the main memory to the DB
                        self.movies.insert_many(movies_list, ordered=False)
                        movies_list = list()
            else:  # Invalid file extension. Do not populate
                print("Invalid file extension {}. Will not populate...".format(ext))
                return

    def _process_imdb_movie(self, movie_object):
        movie = {
            '_id': movie_object['id'],
            'title': movie_object['title'],
            'cast': []
        }
        for attr in ['description', 'year', 'rating', 'countOfRatings', 'categories', 'thumbnail', 'plotKeywords']:
            if attr in movie_object:  # check for existence before adding
                movie[attr] = movie_object[attr]

        for actor in movie_object['cast'].keys():
            movie['cast'].append({
                'actor': actor,
                'character': movie_object['cast'][actor]
            })
        return movie





    def splits_per_term(self, term: str):
        return self.inverted_index.count_documents({"term": term})

    def get_indexed_documents_by_term(self, term: str, skip: int, limit: int):
        docs_for_term = self.inverted_index.find({"term": term}, {"_id": 0}).skip(skip).limit(limit)
        return docs_for_term

    def get_movie_ids_advanced_search(self, query_params:dict):
        movies_set = set()
        if query_params.get('movie_title'):
            if query_params.get('year'):
                year = re.split('-', query_params['year'])
                if query_params.get('actor'):
                    movie = self.movies.find_one({"$and" :[{"title": query_params['movie_title']}, {"year": {"$gte": int(year[0]), "$lte": int(year[1])}}, {"cast.actor": query_params['actor']}]},{"_id": 1})
                    movies_set.add(movie.get("_id"))
                else:
                    movie = self.movies.find_one({"$and": [{"title": query_params['movie_title']}, {"year": {"$gte": int(year[0]), "$lte": int(year[1])}}]},{"_id": 1})
                    movies_set.add(movie.get("_id"))
            else:
                movie = self.movies.find_one({"title": query_params['movie_title']},{"_id": 1})
                movies_set.add(movie.get("_id"))
        elif query_params.get('year'):
            year = re.split('-', query_params['year'])
            if query_params.get('actor'):
                movies = list(self.movies.find({"$and": [{"year": {"$gte": int(year[0]), "$lte": int(year[1])}}, {"cast.actor": query_params['actor']}]},{"_id": 1}))
                return set(map(itemgetter('_id'), movies))
            else:
                movies = list(self.movies.find({"year": {"$gte": int(year[0]), "$lte": int(year[1])}},{"_id": 1}))
                return set(map(itemgetter('_id'), movies))
        else:
            movies = list(self.movies.find({"cast.actor": query_params['actor']},{"_id": 1}))
            return set(map(itemgetter('_id'), movies))
        return movies_set
