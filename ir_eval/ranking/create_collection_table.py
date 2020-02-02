import json
import pickle
import numpy as np
import sys
import time

def json_load(path):
    """ It loads and returns a json data in dictionary structure.

    Arguments:
        path {string} -- the path of the json data

    Returns:
        dictionary -- the dictionary created from the json data.
    """
    return json.load(open(path))

def create_small_index():
	doc_nums = [list(inverted_index[word].keys())[0] for word in inverted_index.keys()]
	doc_nums = doc_nums[0:10000]
	inverted_index_small = {}
	for word in inverted_index:
		for doc in inverted_index[word]:
			if doc in doc_nums:
				inverted_index_small[word] = {}
				inverted_index_small[word][doc] = inverted_index[word][doc]

	with open('inverted_index_small.pickle', 'wb') as handle:
		pickle.dump(inverted_index_small, handle, protocol=pickle.HIGHEST_PROTOCOL)


def create_term_doc_collection(inverted_index, doc_nums):
    """Create a term-document incident collection that shows which documents each term belongs to
    Args:
        inverted_index (dict): Index of terms as keys and dict of documents with positions as values
        doc_nums (list): An array of the documents numbers
    Returns:
        collection_dict (dict): A boolean vector for each word
    """
    words = list(inverted_index.keys())
    collection_dict = dict()
    boolean_matrix = np.zeros((len(words), len(doc_nums)), dtype=np.bool)

    # Create a mapping of document numbers to continuous indices from 0 to len(doc_nums)-1
    doc_num_dict = {}
    for ind, doc_num in enumerate(doc_nums):
        doc_num_dict[doc_num] = ind

    for i, word in enumerate(words):
        docs_for_specific_word = list(inverted_index[word].keys())

        for index, doc_num in enumerate(docs_for_specific_word):
            if doc_num in list(doc_num_dict.keys()):
                doc_id = doc_num_dict[doc_num]
                boolean_matrix[i][int(doc_id)] = True

        collection_dict[word] = boolean_matrix[i]

    return collection_dict


t0 = time.time()

inverted_index = json_load('inverted_index_file/inverted_index.json')
print('create small index')
create_small_index()
with open('inverted_index_small.pickle', 'rb') as handle:
	inverted_index = pickle.load(handle)

print(' create doc nums')
doc_nums = [list(inverted_index[word].keys())[0] for word in inverted_index.keys()]
#doc_nums = doc_nums[0:3000]

print('start collection matrix')
collection_dict = create_term_doc_collection(inverted_index, doc_nums)

with open('collection_dict.pickle', 'wb') as handle:
	pickle.dump(collection_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


t1 = time.time()

print(t1-t0)




