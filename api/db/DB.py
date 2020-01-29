from db.ShelveDB import ShelveDB
from db.MongoDB import MongoDB
from db.DBInterface import DBInterface
from flask import Flask



def get_db_instance():
	return MongoDB()


def get_db_instance_ShelveDB():
	return ShelveDB()

