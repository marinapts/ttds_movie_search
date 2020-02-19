from typing import List
from flask_pymongo import PyMongo
from pymongo import MongoClient
from db.DBInterface import DBInterface
import gridfs
import json
import re
from operator import itemgetter

class MongoDB(DBInterface):

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

    def get_all_quote_ids(self):
        word_list = [list(element.values())[0] for element in list(self.sentences.find({}, {"$id": 1}))]
        return quote_ids

    def get_all_words(self):
        word_list = [list(element.values())[0] for element in list(self.inverted_index.find({}, {"$id": 1}))]
        return word_list

    def get_index_docs_by_word(self, word: str):
        doc_list = list(self.inverted_index.find({"_id": word}, {"_id": 0}))
        if len(doc_list) != 0:
            doc_list = doc_list[0]
        return doc_list

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
        raise NotImplementedError()

    def splits_per_term(self, term: str):
        return self.inverted_index.count_documents({"term": term})

    def get_indexed_documents_by_term(self, term: str, skip: int):
        docs_for_term = list(self.inverted_index.find({"term": term}, {"_id": 0}).skip(skip).limit(1))[0]
        return docs_for_term


    def get_movie_ids_advanced_search(self, query_params:dict):
        movie_list = []
        if query_params.get('movie_title'):
            if query_params.get('year'):
                year = re.split('-', query_params['year'])
                if query_params.get('actor'):
                    movie = self.movies.find_one({"$and" :[{"title": query_params['movie_title']}, {"year": {"$gte": int(year[0]), "$lte": int(year[1])}}, {"cast.actor": query_params['actor']}]},{"_id": 1})
                    movie_list.append(movie.get("_id"))
                else:
                    movie = self.movies.find_one({"$and": [{"title": query_params['movie_title']}, {"year": {"$gte": int(year[0]), "$lte": int(year[1])}}]},{"_id": 1})
                    movie_list.append(movie.get("_id"))
            else:
                movie = self.movies.find_one({"title": query_params['movie_title']},{"_id": 1})
                movie_list.append(movie.get("_id"))
        elif query_params.get('year'):
            year = re.split('-', query_params['year'])
            if query_params.get('actor'):
                movie = list(self.movies.find({"$and": [{"year": {"$gte": int(year[0]), "$lte": int(year[1])}}, {"cast.actor": query_params['actor']}]},{"_id": 1}))
                return list(map(itemgetter('_id'), movie))
            else:
                movie = list(self.movies.find({"year": {"$gte": int(year[0]), "$lte": int(year[1])}},{"_id": 1}))
                return list(map(itemgetter('_id'), movie))
        else:
            movie = list(self.movies.find({"cast.actor": query_params['actor']},{"_id": 1}))
            return list(map(itemgetter('_id'), movie))
        return movie_list
