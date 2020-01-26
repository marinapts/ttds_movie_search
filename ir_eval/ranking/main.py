import json
import pickle
import numpy as np


def json_load(path):
    """ It loads and returns a json data in dictionary structure.

    Arguments:
        path {string} -- the path of the json data

    Returns:
        dictionary -- the dictionary created from the json data.
    """
    return json.load(open(path))


def load_file_binary(file_name):
    with open(file_name + '.pickle', 'rb') as f:
        return pickle.load(f)


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
            doc_id = doc_num_dict[doc_num]
            boolean_matrix[i][int(doc_id)] = True

        collection_dict[word] = boolean_matrix[i]

    return collection_dict


def TFIDF(document, terms, N, inverted_index):
    """Calculates the retrieval score using the TFIDF (term frequency - inverse document frequency) formula
    Args:
        document (str)
        terms (list)
        N (list): Total number of documents
        inverted_index (dict)
    Returns:
        total_score (float): Retrieval score for a query and a document
    """
    total_score = 0

    # For each term calculate the tf (term frequency in doc) and df (number of docs that word appeared in)
    for term in terms:
        # Check if the document includes the term
        if document in inverted_index[term].keys():
            # Frequency of term in this document
            tf = len(inverted_index[term][document])
            # Number of documents in which the term appeared
            df = len(inverted_index[term].keys())
            term_weight = (1 + np.log10(tf)) * np.log10(N / df)
            total_score += term_weight

    return total_score


def array_to_string(arr):
    array_str = ''

    for i in arr:
        array_str += '{}, '.format(i)
    return array_str


def boolean_search(query_str_transformed, doc_nums):
    """Performs boolean search for one or more combinations of terms.
    Args:
        query_str_transformed (str): A string representation of the AND, OR and NOT used between numpy arrays
        doc_nums (list)
    Returns:
        documents (list): The resulting documents of the boolean search
    """
    doc_num_mapping = {}  # Map doc numbers to continuous indices

    for ind, doc_num in enumerate(doc_nums):
        doc_num_mapping[ind] = doc_num

    # Use eval to evaluate the boolean search
    boolean_vector = eval(query_str_transformed)
    documents = [doc_num_mapping[i] for i in range(len(boolean_vector)) if boolean_vector[i] == True]
    return documents


def ranked_retrieval(queries, collection_table, doc_nums, inverted_index, stop_words):
    """Performs ranked IR based on TFIDF
    Args:
        queries (list): Queries from queries.ranked.txt
        collection_table (dict)
        doc_nums (list)
        inverted_index (dict)
        stop_words (list)
    Returns:
        ranked_scores (list): The resultsing documents and the score for each ranked query
    """
    print('Starting ranked retrieval...')
    ranked_scores = {}

    for query_index, query_tokens in enumerate(queries):
        # Convert query into an OR boolean search and use eval to evaluate it
        boolean_vectors = []
        for token in query_tokens:
            boolean_vector = collection_table[token]
            boolean_vectors.append('np.array([{}])'.format(array_to_string(boolean_vector)))

        query_eval_string = ' | '.join(boolean_vectors)
        query_documents = boolean_search(query_eval_string, doc_nums)

        query_scores = []
        # Map query_boolean_result to a list of document ids
        for doc in query_documents:
            score = TFIDF(doc, query_tokens, len(doc_nums), inverted_index)
            query_scores.append((doc, score))

        # Sort scores for each query on a descending order
        query_scores = sorted(query_scores, key=lambda x: x[1], reverse=True)
        ranked_scores[query_index + 1] = query_scores

    return ranked_scores


if __name__ == '__main__':
    inverted_index = json_load('../inverted_index.json')
    # @TODO: Get quotes and quote ids
    doc_nums = []   # A list of all the document numbers

    # Create a term-document incident collection that shows which documents each term belongs to
    collection_table = create_term_doc_collection(inverted_index, doc_nums)
    # @TODO: Save collection table in DB or as a file

    # Ranked search
    # ranked_retrieval_results = ranked_retrieval(queries_ranked, collection_table, doc_nums, inverted_index, stop_words)
    # save_ranked_retrieval_results(ranked_retrieval_results, RESULTS_RANKED_FILE)

