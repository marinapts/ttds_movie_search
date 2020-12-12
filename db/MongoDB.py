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
        client = MongoClient('INSERT_YOUR_OWN_IP', 27017, username='INSERT_YOUR_OWN_USERNAME', password='INSERT_YOUR_OWN_PASSWORD')
        self.ttds = client.ttds
        self.sentences = self.ttds.sentences
        self.inverted_index = self.ttds.inverted_index
        self.movies = self.ttds.movies
        self.sentences.create_index('_id')
        self.inverted_index.create_index('_id')
        self.movies.create_index('_id')
        self.inverted_index_gridfs = gridfs.GridFS(self.ttds)


    def get_quotes_by_list_of_quote_ids(self, ids: List[int]):
        # Given a list of quote ids, return a list of quote dictionaries, sorted in the same order that the ids are provided.
        quote_list = list(self.sentences.find({"_id": {"$in": ids}}))
        # Sort results from mongodb by the ids list, since the order is not maintained
        sorted_quote_dict = {d['_id']: d for d in quote_list}  # sentence_id -> sentence_dict
        sorted_quote_list = [sorted_quote_dict[i] for i in ids]
        return sorted_quote_list

    def get_quotes_by_movie_id(self, movie_id: str):
        # Given a movie id, returns a list of all sentences in that movie
        quote_list = list(self.sentences.find({"movie_id": movie_id}))
        return quote_list

    def get_movie_by_id(self, id):
        return self.movies.find_one({'_id': id})

    def get_movies_by_list_of_ids(self, ids: List[str]):
        # Given a list of movie ids, return a list of movie dictionaries, sorted in the same order that the ids are provided.
        movie_list = list(self.movies.find({"_id": {"$in": ids}}, {  # return only fields that are displayed in the list.
            '_id': 1,
            'title': 1,
            'categories': 1,
            'thumbnail': 1,
            'plotKeywords': 1  # this will have to be cleaned later before returning the results
        }))  # full movie information can be retrieved via get_movie_by_id()
        # Sort results from mongodb by the ids list, since the order is not maintained
        movie_id_to_movie = {d['_id']: d for d in movie_list}
        sorted_movie_list = [movie_id_to_movie[id] for id in ids]
        return sorted_movie_list

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

    def get_indexed_documents_by_term(self, term: str, skip: int, limit: int, sort_entries: bool = False):
        docs_for_term = self.inverted_index.find({"term": term}, {"_id": 0})
        if sort_entries:
            docs_for_term = docs_for_term.sort('movies.0._id')
        docs_for_term = docs_for_term.skip(skip).limit(limit)
        return docs_for_term

    def get_indexed_movies_by_term(self, term: str):
        return self.inverted_index.find({"term": term}, {"movies.sentences": 0})

    def get_movie_ids_advanced_search(self, query_params: dict):
        and_list = []
        if query_params.get('movie_title', False):
            and_list.append({"title": query_params['movie_title'].title()})
        if query_params.get('year', False):
            try:  # this may crash, so careful
                year = re.split('-', query_params['year'])
                and_list.append({"year": {"$gte": int(year[0]), "$lte": int(year[1])}})
            except:
                print(f"Attempted to make advanced search with invalid year: {query_params['year']}")
        if query_params.get('actor', False):
            and_list.append({"cast.actor": query_params['actor'].title()})
        if query_params.get('categories', False):
            try:
                categories = re.split(',', query_params['categories'].title())
                and_list.append({'categories': {'$in': categories}})
            except:
                print(f"Attempted to make advanced search with invalid categories: {query_params['categories']}")
        movies = self.movies.find({"$and": and_list}, {"_id": 1})
        return set(map(itemgetter('_id'), movies))
