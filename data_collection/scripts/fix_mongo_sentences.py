"""
This script updates our MongoDB sentences collection:
The format of _id is changed from "tt0000023_1" to incremental integers (from 0 to ~75000000).
"""

from db.MongoDB import MongoDB
import copy

mongo = MongoDB()
sentences = mongo.sentences
START_ID = 1548894

id = START_ID
while True:
    # s = sentences.find_one({"_id": "tt0000023_1"})
    ss = sentences.find({"_id": {"$type": "string"}}, limit=100000)
    if ss is None:
        break

    updated_sentences = []
    old_ids = []
    for s in ss:
        old_ids.append(s['_id'])
        updated = copy.deepcopy(s)
        updated['_id'] = id
        updated_sentences.append(updated)
        id += 1

    if len(old_ids) == 0:
        break
    print("{} outdated sentences found".format(len(old_ids)))

    result = sentences.insert_many(updated_sentences)
    print("{} inserted (last id: {}).".format(len(result.inserted_ids), max(result.inserted_ids)))
    if len(result.inserted_ids) != len(updated_sentences):
        print("Something went wrong. Not all copied sentences have been saved correctly! Failed sentences:")
        for s in updated_sentences:
            if s['_id'] not in result.inserted_ids:
                print(s)
        print("Aborting...")
        break

    # The documents have been copied. Delete the old documents
    del_result = sentences.delete_many({"_id": {"$in": old_ids}})
    if del_result.deleted_count != len(old_ids):
        print("Failed to delete some outdated sentences! _ids:")
        print(old_ids)
        print("Aborting...")
        break


print("id {} reached".format(id))