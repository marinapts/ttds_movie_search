import io
import preprocessing
import database_functions

unique = set()

cursors = database_functions.get_sentences_cursors()

for cursor in cursors:
    unique.update(preprocessing.preprocess(cursor.get('sentence')))

with open("unique.txt","w") as output:
    output.writelines(unique)
        