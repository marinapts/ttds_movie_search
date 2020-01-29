from typing import List
from abc import ABC, abstractmethod
from flask_pymongo import PyMongo
from pymongo import MongoClient
from db.DBInterface import DBInterface

class MongoDB(DBInterface):

    def __init__(self):
        client = MongoClient('167.71.139.222', 27017, username='admin', password='iamyourfather')
        self.ttds = client.ttds
        self.sentences = self.ttds.sentences

    def get_quotes_by_list_of_quote_ids(self, ids: List[str]):
        quote_list = [self.sentences.find_one({"_id": idd}) for idd in ids]
        return quote_list

    def get_movies_by_list_of_ids(self, ids: List[str]):
        # Given a list of movie ids, return a list of movie dictionaries
        raise NotImplementedError()

    def populate_movies_data(self, file_path: str, clear: bool):
        # Given a file with movies data, populate the database with those movies.
        # File can be either .json or .jsonl
        # clear flag specifies whether all contents of the database should be cleared before populating.
        raise NotImplementedError()

