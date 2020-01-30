import shelve, atexit, json
from typing import List
from db.DBInterface import IndexDBInterface

DB_PATH = 'db/data/shelve'


class ShelveDB(IndexDBInterface):

    d = None

    def __init__(self, write_mode=False):
        super().__init__()
        # Initialise dbm if it does not exist yet
        c = shelve.open(DB_PATH, flag='c')
        c.close()
        # Now, open a read-only shelf (or with write privileges if write_mode=True).
        self.d = shelve.open(DB_PATH, flag=('r' if not write_mode else 'c'))
        atexit.register(self.d.close)

    def get_index_by_term(self, term: str):
        return self.d.get(term)

    def add_index_for_term(self, term: str, index):
        self.d[term] = index
