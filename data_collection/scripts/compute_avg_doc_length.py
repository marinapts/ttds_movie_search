"""
This script computes the average processed (stop words removed) sentence length based on the sentences collection.
"""

from db.MongoDB import MongoDB
from pymongo.operations import UpdateMany
from collections import defaultdict
import pprint
import csv
from ir_eval.preprocessing import preprocess

START_TOTAL_LENGTH = 0
START_COUNT = 0

mongo = MongoDB()
sentences = mongo.sentences
total_length = START_TOTAL_LENGTH
LIMIT = 100000


total_counted = START_COUNT
while True:
    ss = sentences.find({}, {"sentence": 1, "_id": 0}, skip=total_counted, limit=LIMIT)
    if ss is None:
        break

    for s in ss:
        total_length += len(preprocess(s['sentence']))
        total_counted += 1

    print("Count: {}\nTotal length: {}\n".format(total_counted, total_length))
    if total_counted % LIMIT != 0:
        break

print("Finished.")

print("Average: {}".format(1.0*total_length/total_counted))
