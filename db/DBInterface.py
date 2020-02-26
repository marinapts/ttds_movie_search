from typing import List
from abc import ABC, abstractmethod


class DBInterface(ABC):
    # All Database getter methods will return Python dictionary objects (or a list of Python dictionary objects)

    def __init__(self):
        # Some initialisation can be done here in an implementing class
        pass

    @abstractmethod
    def get_quotes_by_list_of_quote_ids(self, ids: List[int]):
        # Given a list of quote ids, return a list of quote dictionaries
        raise NotImplementedError()

    @abstractmethod
    def get_quotes_by_movie_id(self, movie_id: str):
        # Given a movie id, returns a list of all sentences in that movie
        raise NotImplementedError()

    @abstractmethod
    def get_movies_by_list_of_ids(self, ids: List[str]):
        # Given a list of movie ids, return a list of movie dictionaries
        raise NotImplementedError()

    @abstractmethod
    def populate_movies_data(self, file_path: str, clear: bool):
        # Given a file with movies data, populate the database with those movies.
        # File can be either .json or .jsonl
        # clear flag specifies whether all contents of the database should be cleared before populating.
        raise NotImplementedError()

    @abstractmethod
    def splits_per_term(self, term: str):
        # Return the splits that each term has.
        return NotImplementedError()

    @abstractmethod
    def get_indexed_documents_by_term(self, term: str, skip: int, limit: int, sort_entries: bool = False):
        # Given a term, returns an iterable of inverted index entries
        raise NotImplementedError()

    @abstractmethod
    def get_indexed_movies_by_term(self, term: str):
        # Given a term, returns an iterable of inverted index entries without sentences
        raise NotImplementedError()

    @abstractmethod
    def get_movie_ids_advanced_search(self, query_params:dict):
        # Given a query parameters for advanced search, returns a list of movie ids
        raise NotImplementedError()
