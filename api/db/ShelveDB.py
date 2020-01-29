import shelve, atexit, json
from typing import List
from db.DBInterface import DBInterface

DB_PATH = 'db/data/shelve'

class ShelveDB(DBInterface):

    d = None

    def __init__(self):
        # Initialise dbm if it does not exist yet
        c = shelve.open(DB_PATH, flag='c')
        c.close()
        # Now, open a read-only shelf.
        self.d = shelve.open(DB_PATH, flag='r')
        atexit.register(self.d.close)

    def get_quotes_by_list_of_quote_ids(self, ids: List[str]):
        return NotImplementedError()

    def get_movies_by_list_of_ids(self, ids: List[str]):
        return [self.d.get(id) for id in ids]

    def populate_movies_data(self, file_path: str, clear: bool = False):
        with shelve.open(DB_PATH, flag='c') as db_write_mode:
            with open(file_path, 'r') as file:
                ext = file_path.split('.')[-1]
                if ext == 'json':  # JSON format - the whole file is a JSON list of movies
                    movies = json.load(file)
                    for movie in movies:
                        db_write_mode[movie['id']] = movie
                elif ext == 'jsonl':  # JSON Lines format - each line is a JSON object
                    for line in file:
                        movie = json.loads(line)
                        db_write_mode[movie['id']] = movie
                else:  # Invalid file extension. Do not populate
                    print("Invalid file extension {}. Will not populate...".format(ext))

