from typing import List
from flask_pymongo import PyMongo
from pymongo import MongoClient
from db.DBInterface import DBInterface
import gridfs
import json

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

    def get_indexed_documents_by_term(self, term: str):
        if self.inverted_index_gridfs.exists(term):
            return json.loads(self.inverted_index_gridfs.get(term).read().decode('utf-8'))
        else:
            return dict()


