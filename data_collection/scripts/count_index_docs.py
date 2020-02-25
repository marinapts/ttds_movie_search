"""
This script updates our MongoDB inverted_index collection:
The doc_count is changed to the aggregate sum of all doc_counts of the same term.
"""

from db.MongoDB import MongoDB
from pymongo.operations import UpdateMany
from collections import defaultdict
import pprint
import csv

mongo = MongoDB()
index = mongo.ttds.inverted_index
terms = defaultdict(int)  # term -> total_docs
LIMIT = 100000


total_counted = 0
while True:
    index_terms = index.find({}, {"term": 1, "doc_count": 1, "_id": 0}, skip=total_counted, limit=LIMIT)
    if index_terms is None:
        break

    for term_doc in index_terms:
        term = term_doc['term']
        count = term_doc['doc_count']
        terms[term] += count
        total_counted += 1



    print(total_counted)
    if total_counted % LIMIT != 0:
        break

with open('terms.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, ['term', 'count'])
    writer.writeheader()
    for t in terms.keys():
        writer.writerow({'term': t, 'count': terms[t]})

print("Finished.")
