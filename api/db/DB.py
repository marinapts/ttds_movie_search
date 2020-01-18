from db.ShelveDB import ShelveDB
from db.DBInterface import DBInterface


def get_db_instance() -> DBInterface:
    # If we want to use other DB, e.g. MongoDB, replace the return statement below.
    return ShelveDB()
