"""
This script computes the average processed (stop words removed) sentence length based on the sentences collection.
"""

from db.MongoDB import MongoDB
import io
import csv

# Change this to the number of sentences already processed if you want to resume the script.
START_COUNT = 0

mongo = MongoDB()
sentences = mongo.sentences
LIMIT=100000
output_file = io.open('sentences.csv', mode='a+', encoding='utf-8', newline='')
output = csv.DictWriter(output_file, fieldnames=['_id', 'movie_id', 'sentence'])
output.writeheader()

total_processed = START_COUNT
try:
    while True:
        ss = sentences.find({}, {"sentence": 1, "_id": 1, 'movie_id': 1}, skip=total_processed)
        if ss is None:
            print("END OF SENTENCES REACHED!")
            break

        for s in ss:
            output.writerow({
                '_id': s['_id'],
                'movie_id': s['movie_id'],
                'sentence': s['sentence']
            })
            total_processed += 1
            if total_processed % LIMIT == 0:
                print(f"{total_processed} sentences downloaded.")

        print("{} sentences have been downloaded so far".format(total_processed))
        if total_processed % LIMIT != 0:
            print("END OF SENTENCES REACHED!")
            break
except:
    pass

print(f"Finished. If you want to resume the script, set START_COUNT to {total_processed}")
