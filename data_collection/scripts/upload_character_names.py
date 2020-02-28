"""
This script uploads character names for sentences that we have the names for (thanks to Oguz).
"""

from db.MongoDB import MongoDB
from pymongo.operations import UpdateOne
import io
import csv

# Change this to the number of sentences already processed if you want to resume the script.
START_COUNT = 0
WRITE_LIMIT = 10000

mongo = MongoDB()
sentences = mongo.sentences
ops = []
total_written = 0
total_read = 0

def write_character_name(sentence_id, character_name):
    ops.append(UpdateOne({'_id': sentence_id}, {'$set': {'character': character_name}}))
    if len(ops) >= WRITE_LIMIT:
        flush_ops()

def flush_ops():
    global total_written
    sentences.bulk_write(ops)
    total_written += len(ops)
    ops.clear()
    print(f"{total_written} sentences written.")


try:
    for i in range(4):  # 4 files
        file = io.open(f'quote_match_{i}.csv', 'r', encoding='utf-8')
        reader = csv.reader(file)
        for line in reader:
            id = int(line[0].strip())
            character = line[1].strip()
            total_read += 1
            if total_read >= START_COUNT:
                write_character_name(id, character)
except:
    print("Caught an exception.")


flush_ops()

print(f"Finished. If you want to resume the script, set START_COUNT to {total_written}")
