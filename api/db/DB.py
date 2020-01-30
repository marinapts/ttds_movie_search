from db.ShelveDB import ShelveDB
from db.MongoDB import MongoDB
from db.DBInterface import DBInterface


def get_db_instance() -> DBInterface:
    return MongoDB()


# deprecated
def get_db_instance_ShelveDB() -> DBInterface:
    return ShelveDB()
