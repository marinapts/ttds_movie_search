from db.ShelveDB import ShelveDB
from db.MongoDB import MongoDB
from db.DBInterface import DBInterface, IndexDBInterface


def get_db_instance() -> DBInterface:
    return MongoDB()


def get_index_db_instance(write_mode=False) -> IndexDBInterface:
    return ShelveDB(write_mode=write_mode)
