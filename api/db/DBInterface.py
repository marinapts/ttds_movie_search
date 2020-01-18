from typing import List
from abc import ABC, abstractmethod


class DBInterface(ABC):
    # All Database getter methods will return Python dictionary objects (or a list of Python dictionary objects)

    def __init__(self):
        # Some initialisation can be done here in an implementing class
        pass

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
