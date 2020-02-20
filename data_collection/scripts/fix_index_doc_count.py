"""
This script updates our MongoDB inverted_index collection:
The doc_count is changed to the aggregate sum of all doc_counts of the same term.
Requirements:
Use script `count_index_docs.py` to generate a csv file containing all the terms and their total doc_counts.
"""

from db.MongoDB import MongoDB
from pymongo.operations import UpdateMany
import csv

mongo = MongoDB()
index = mongo.ttds.inverted_index
batch_terms = dict()  # term -> total_docs
BATCH_SIZE = 1000
last_term = None


def write_batch(term_dict):
    ops = [UpdateMany({"term": t}, {"$set": {'doc_count': term_dict[t]}}) for t in term_dict.keys()]
    bulk_write_result = index.bulk_write(ops)
    print("{} updated.".format(bulk_write_result.matched_count))
    return bulk_write_result.matched_count


file = open('terms.csv', mode='r')
reader = csv.DictReader(file)

total_updated = 0
last_term_found = False
latest_term = ''
for row in reader:
    if last_term is not None and last_term_found is False:
        if row['term'] == last_term:
            last_term_found = True
        continue
    batch_terms[row['term']] = int(row['count'])
    latest_term = row['term']

    if len(batch_terms) % BATCH_SIZE == 0:
        # Flush the batch
        total_updated += write_batch(batch_terms)
        batch_terms.clear()
        print("Total (after term {}): {}".format(latest_term, total_updated))

# Final batch
total_updated += write_batch(batch_terms)
print("Total: {}\nFinished.".format(total_updated))
