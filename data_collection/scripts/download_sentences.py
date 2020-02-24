"""
This script computes the average processed (stop words removed) sentence length based on the sentences collection.
"""

from db.MongoDB import MongoDB
import io

# Change this to the number of sentences already processed if you want to resume the script.
START_COUNT = 0

mongo = MongoDB()
sentences = mongo.sentences
LIMIT = 100000
output = io.open('sentences.txt', mode='a+', encoding='utf-8')

total_processed = START_COUNT
try:
    while True:
        ss = sentences.find({}, {"sentence": 1, "_id": 0}, skip=total_processed, limit=LIMIT)
        if ss is None:
            print("END OF SENTENCES REACHED!")
            break

        for s in ss:
            output.write(f"{s['sentence']}\n")
            total_processed += 1

        output.flush()
        print("{} sentences have been downloaded so far".format(total_processed))
        if total_processed % LIMIT != 0:
            print("END OF SENTENCES REACHED!")
            break
except:
    pass

output.flush()
output.close()
print(f"Finished. If you want to resume the script, set START_COUNT to {total_processed}")
