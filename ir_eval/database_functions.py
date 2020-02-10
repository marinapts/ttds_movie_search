import pymongo

from pymongo import MongoClient

client = MongoClient('mongodb://admin:iamyourfather@167.71.139.222:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
#client = MongoClient('mongodb://admin:iamyourfather@127.0.0.1:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')

db = client.ttds
sent = db.sentences
inverted_index_stop = db.inverted_index_with_stop
inverted_index = db.inverted_index

sentence_bson_list = list()
previous_id = -1

def get_max_sent_id():
    return sent.find_one({"_id": {"$exists": True}}, sort=[("_id", -1)])["_id"]

def update_sentences(data, title):
    global previous_id
    if previous_id == -1:
        previous_id = get_max_sent_id()

    for line_number, line in enumerate(data, start=1):
        previous_id += 1
        sentence_bson_list.append({"_id":previous_id, "sentence": line[1], "time_ms": line[0], "movie_id": title})
        
        if len(sentence_bson_list) == 100000:
            sent.insert_many(sentence_bson_list)
            sentence_bson_list.clear()

def get_sentences_cursors():
    #return sent.find({'movie_id':'tt0080684'})
    return sent.find()

def update_inverted_index_stop(term, doc_id, position):
    inverted_index_stop.update({ '_id': term}, { '$addToSet': {"docs.$._id": doc_id, 'docs.$.pos': position}}, True)

def update_inverted_index(term, doc_id, position):
    inverted_index.update({'_id': term}, { '$push': { doc_id : position } }, True)
