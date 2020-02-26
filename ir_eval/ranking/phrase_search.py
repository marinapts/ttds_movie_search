import pickle
from db.DB import get_db_instance
import time
from pathlib import Path
from collections import defaultdict

MAX_INDEX_SPLITS = 52  # maximum number of different entries in the inverted_index with the same term
BATCH_SIZE = 52
MAX_QUERY_TIME = 100  # max seconds to allow the query to run for
MIN_RATINGS = 100
movie_ratings = defaultdict(lambda: MIN_RATINGS)
try:
    ratings_path = Path(__file__).parent.absolute() / 'pickles' / 'movie_ratings.p'
    movie_ratings = defaultdict(lambda: MIN_RATINGS, pickle.load(open(ratings_path, 'rb')))
except:
    print("No valid pickle file with movie ratings found. Weighted quote phrase search may not work properly...")

db = get_db_instance()

def phrase_search(query_params, number_results):
    """ This function should be called by app.py to perform a phrase search
    """
    assert len(query_params['query']) > 1, "phrase search should not be used for queries with only one term. Use BM25 instead."
    results = query_phrase_search(query_params)
    return results[:number_results]

def query_phrase_search(query_params):
    """
    Phrase search finds all sentences containing the exact phrase specified in query_params, and returns a list of
    sentence _ids sorted by iMDB count of ratings (in descending order), reflecting popularity.
    """
    results = []
    terms = query_params['query']
    # Prepare advanced search if any filters are provided
    filtered_movies = None
    if len(query_params['movie_title']) > 0 or len(query_params['year']) > 0 or len(query_params['actor']) > 0:
        print('advanced search')
        filtered_movies = db.get_movie_ids_advanced_search(query_params)

    cursors = []
    for dist, term in enumerate(terms):
        cursor = db.get_indexed_documents_by_term(term, 0, BATCH_SIZE)
        index = next(cursor, None)
        cursors.append({
            'cursor': cursor,
            'index': index,
            'm': 0,  # movie index
            's': 0,  # sentence index
            'p': 0  # position index,
        })

    # while all(c['index'] is not None for c in cursors):  # continue until at least one cursor is fully exhausted
    start_time = time.time()
    while True:  # continue until at least one cursor is fully exhausted
        for i in range(len(cursors) - 1):
            cur_i = cursors[i]
            cur_j = cursors[i+1]
            # catch up j with i
            exhausted = catchup(cur_j, cur_i)
            if exhausted:  # cur_j has been exhausted so there's no point in trying to find any more matches, abort.
                return order_results_by_popularity(results)
        # At this point, the term cursors should be ordered, e.g. "i" < "am" < "your" < "father".
        # Check if an exact phrase match was found.
        phrase_found = True
        start_cur = cursors[0]
        start_mov = start_cur['index']['movies'][start_cur['m']]
        start_sen = start_mov['sentences'][start_cur['s']]
        start_pos = start_sen['pos'][start_cur['p']]

        for i in range(1, len(cursors)):
            cur = cursors[i]
            if cur['index']['movies'][cur['m']]['_id'] != start_mov['_id'] or \
                    cur['index']['movies'][cur['m']]['sentences'][cur['s']]['_id'] != start_sen['_id'] or \
                    cur['index']['movies'][cur['m']]['sentences'][cur['s']]['pos'][cur['p']] - start_pos != i:
                phrase_found = False
                break
        if phrase_found and (filtered_movies is None or start_mov['_id'] in filtered_movies):  # supports advanced search
            results.append({
                'movie_id': start_mov['_id'],
                'sentence_id': start_sen['_id']
            })
        # # Done. Now advance the first cursor ("i") to catch up with the last cursor ("father").
        end_cur = cursors[-1]
        end_mov = end_cur['index']['movies'][end_cur['m']]
        end_sen = end_mov['sentences'][end_cur['s']]
        end_pos = end_sen['pos'][end_cur['p']]
        if start_mov['_id'] < end_mov['_id']:
            advance_cursor_iterator(start_cur, 'm')
        if start_mov['_id'] == end_mov['_id'] and start_sen['_id'] < end_sen['_id']:
            advance_cursor_iterator(start_cur, 's')
        if start_mov['_id'] == end_mov['_id'] and start_sen['_id'] == end_sen['_id'] and start_sen['pos'][start_cur['p']] < end_pos:
            advance_cursor_iterator(start_cur, 'p')

        if start_cur['cursor'] is None or time.time() - start_time > MAX_QUERY_TIME:
            return order_results_by_popularity(results)


def order_results_by_popularity(results):
    return list(map(lambda r: r['sentence_id'], sorted(results, key=lambda r: movie_ratings[r['movie_id']], reverse=True)))


def advance_cursor_iterator(cursor, which):
    # which can be either 'm', 's', 'p', or 'i' (for 'index')
    if cursor['index'] is None:
        return
    if which == 'p':
        cursor['p'] += 1
        if cursor['p'] >= len(cursor['index']['movies'][cursor['m']]['sentences'][cursor['s']]['pos']):
            cursor['p'] = 0
            which = 's'
    if which == 's':
        cursor['s'] += 1
        cursor['p'] = 0
        if cursor['s'] >= len(cursor['index']['movies'][cursor['m']]['sentences']):
            cursor['s'] = 0
            which = 'm'
    if which == 'm':
        cursor['m'] += 1
        cursor['s'] = 0
        cursor['p'] = 0
        if cursor['m'] >= len(cursor['index']['movies']):
            cursor['m'] = 0
            which = 'i'
    if which == 'i':
        cursor['index'] = next(cursor['cursor'], None)
        cursor['m'] = 0
        cursor['s'] = 0
        cursor['p'] = 0


def catchup(cur_from, cur_to):
    # cur_from is behind cur_to if the movie_id, sentence_id or position of cur_from is lower than cur_to
    while cur_from['index']['movies'][cur_from['m']]['_id'] < cur_to['index']['movies'][cur_to['m']]['_id']:
        # advance movie iterator
        advance_cursor_iterator(cur_from, 'm')
        if cur_from['index'] is None:
            return True  # True means that the cursor has been exhausted (no more index entries)

    movie_from = cur_from['index']['movies'][cur_from['m']]
    movie_to = cur_to['index']['movies'][cur_to['m']]
    if movie_from['_id'] == movie_to['_id']:
        # caught up with the movie and a movie match was found. Now catch up with the sentence
        while movie_from['sentences'][cur_from['s']]['_id'] < movie_to['sentences'][cur_to['s']]['_id']:
            # advance sentence iterator
            advance_cursor_iterator(cur_from, 's')
            if cur_from['index'] is None:
                return True  # True means that the cursor has been exhausted (no more index entries)
            if cur_from['s'] == 0:  # end of sentences has been reached
                return False  # there's no way we'll have a movie match now (movie_from > movie_to), catch up is done.

    sen_from = movie_from['sentences'][cur_from['s']]
    sen_to = movie_to['sentences'][cur_to['s']]
    if movie_from['_id'] == movie_to['_id'] and sen_from['_id'] == sen_to['_id']:
        # caught up with the movie and sentence. Now catch up with the position
        while sen_from['pos'][cur_from['p']] < sen_to['pos'][cur_to['p']]:
            advance_cursor_iterator(cur_from, 'p')
            if cur_from['index'] is None:
                return True  # True means that the cursor has been exhausted (no more index entries)
            if cur_from['p'] == 0:  # end of positions reached
                return False

    return False


if __name__ == '__main__':

    # query_params = {'query': ['i', 'father'], 'movie_title': '', 'year': '', 'actor': ''}
    query_params = {'query': ['i', 'father'], 'movie_title': '', 'year': '', 'actor': ''}
    start = time.time()
    results = query_phrase_search(query_params)
    end = time.time()
    print(f"Basic phrase search took {end-start} s")
    print(results[:10], len(results))
    # print(258464 in results)
    print(8777416 in results)

    # query_params = {'query': ['i', 'father'], 'movie_title': '', "year": "1980-1981", 'actor': ''}
    query_params = {'query': ['togeth', 'utopia'], 'movie_title': '', "year": "1933-1934", 'actor': ''}
    start = time.time()
    results = query_phrase_search(query_params)
    end = time.time()
    print(f"Advanced phrase search took {end-start} s")
    print(results[:10], len(results))
    print(258464 in results)
    # print(8777416 in results)
