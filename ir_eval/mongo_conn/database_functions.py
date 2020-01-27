#!/usr/bin/env python

import pymongo

from pymongo import MongoClient

client = MongoClient('mongodb://admin:iamyourfather@167.71.139.222:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')

db = client.ttds

sent = db.sentences

def update_db(data, title):
    for line_number, line in enumerate(data, start=1):
        docid = title + '_' + str(line_number)
        json_data = {"_id": docid, "sentence": line[1], "time_ms": line[0], "movie_id": title}
        sent.update({'_id':json_data['_id']}, json_data, True)
        
#sent_id = sent.insert_one({
#    "_id": "tt0000000",
#    "sentence": "sample sentence"
#}).inserted_id

#print(sent_id)

