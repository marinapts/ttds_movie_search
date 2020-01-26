#!/usr/bin/env python

import pymongo

from pymongo import MongoClient

client = MongoClient('mongodb://admin:iamyourfather@167.71.139.222:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')

db = client.ttds

sent = db.sentences


#sent_id = sent.insert_one({
#    "_id": "tt0000000",
#    "sentence": "sample sentence"
#}).inserted_id

#print(sent_id)

