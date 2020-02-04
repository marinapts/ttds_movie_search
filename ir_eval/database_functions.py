import pymongo

from pymongo import MongoClient

client = MongoClient('mongodb://admin:iamyourfather@167.71.139.222:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
#client = MongoClient('mongodb://admin:iamyourfather@127.0.0.1:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')

db = client.ttds
sent = db.sentences
inverted_index_stop = db.inverted_index_with_stop
inverted_index = db.inverted_index

def update_sentences(data, title):
    for line_number, line in enumerate(data, start=1):
        docid = title + '_' + str(line_number)
        json_data = {"_id": docid, "sentence": line[1], "time_ms": line[0], "movie_id": title}
        sent.update({'_id':json_data['_id']}, json_data, True)

def get_sentences_cursors():
    #return sent.find({'movie_id':'tt0080684'})
    return sent.find()

def update_inverted_index_stop(term, doc_id, position):
    inverted_index_stop.update({'_id': term}, { '$push': { doc_id : position } }, True)

def update_inverted_index(term, doc_id, position):
    inverted_index.update({'_id': term}, { '$push': { doc_id : position } }, True)


