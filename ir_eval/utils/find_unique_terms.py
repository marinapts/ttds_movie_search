import csv
from ir_eval.preprocessing import *
from db.MongoDB import MongoDB
from collections import defaultdict
import io

db = MongoDB()
sentences = db.sentences
terms = defaultdict(int)

def write_to_csv(iteration):
    with io.open("terms_{}.csv".format(iteration), mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['term', 'count'])
        writer.writeheader()
        for term in terms.keys():
            writer.writerow({
                'term': term,
                'count': terms[term]
            })

for i in range(1000):
    try:
        ss = sentences.find({}, projection={'_id': False, 'sentence': True}, limit=100000, skip=i*100000)
        if ss is None:
            break

        sth_found = False
        for s in ss:
            sth_found = True
            for t in preprocess(s['sentence']):
                terms[t] += 1

        if not sth_found:
            break
        print("{} processed.".format((i+1)*100000))
        if (i + 1) % 50 == 0:
            write_to_csv((i+1)/10)  # iteration = X Million
    except (KeyboardInterrupt, SystemExit):
        write_to_csv("stopped_i{}".format(i))
        raise

write_to_csv("final")
