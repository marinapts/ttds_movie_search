from flask import Flask, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from db.DB import get_db_instance
import json
from ir_eval.ranking.main import ranked_retrieval
from ir_eval.ranking.movie_search import ranked_movie_search
import re
import time
from ir_eval.preprocessing import preprocess
from api.utils.cache import ResultsCache

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "TTDS Movie Search"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

db = get_db_instance()
cache = ResultsCache.instance()  # Usage: cache.get(query_params), cache.store(query_params, output)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/test')
def testing():
    return 'Hey ttds team, routes seem to be working :)'

def merge_lists(l1, l2, key):
    """ Updates one list with the matching information of the other, using the 'key' parameter.
        Input:
            l1, list to be updated
            l2, list with additional information
            key, matching key between two lists
        Output:
            merged, updated l1 list
    """
    merged = l1
    for n, item1 in enumerate(l1):
        for item2 in l2:
            if item1[key] == item2[key]:
                merged[n].update(item2)
    return merged

def find_categories(results_dict):
    """ Finds categories of retrieved movies and sorts them by frequency
        Input:
            results_dict, results dictionary
        Output:
            list of categories
    """
    category_dict = {}
    for query_result in results_dict:
        if 'categories' in query_result:
            for element in query_result['categories']:
                if element in category_dict.keys():
                    category_dict[element] += 1
                else:
                    category_dict[element] = 0
    category_list = []
    for key in sorted(category_dict, key=category_dict.get, reverse=True):
        category_list.append(key)
    return category_list

def filtering_keywords(query_results, filter_keywords):
    with_keywords = []
    without_keywords = []
    filter_keywords = re.split(',', filter_keywords)
    for query_result in query_results:
        if any(i in filter_keywords for i in query_result['plotKeywords']):
            with_keywords.append(query_result)
        else:
            without_keywords.append(query_result)
    with_keywords.extend(without_keywords)
    return with_keywords

def filtering_title(query_results, filter_title):
    title_match = []
    for query_result in query_results:
        if query_result['title'] == filter_title:
            title_match.append(query_result)
    return title_match

def filtering_years(query_results, filter_years):
    years_match = []
    filter_years = re.split('-', filter_years)
    for query_result in query_results:
        # Some iMDb entries have no 'year' attribute. This will prevent crashes:
        if 'year' not in query_result:  # assume it matches the filter
            years_match.append(query_result)
        elif int(query_result['year']) >= int(filter_years[0]) and int(query_result['year']) <= int(filter_years[1]):
            years_match.append(query_result)
    return years_match

def preprocess_query_params(query_params):
    query_params['query'] = query_params.get('query', '')
    for param in ['movie_title', 'actor', 'keywords', 'year', 'categories']:
        query_params[param] = query_params.get(param, '')  # setting missing params to default empty strings

    query = query_params['query']
    search_phrase = True if query.startswith('"') and query.endswith('"') else False
    # Perform phrase search if the whole query enclosed in quotes and there's at least two terms inside the quotes.
    query = preprocess(query)
    search_phrase = search_phrase and len(query) >= 2  # search phrase must consist of at least 2 terms
    query_params['query'] = query
    query_params['search_phrase'] = search_phrase

    return query_params

@app.route('/movie/<movie_id>')
def find_movie_by_id(movie_id):
    movie = db.get_movie_by_id(movie_id)
    if movie is None:
        return {}, 404
    return movie

@app.route('/query_search', methods=['POST'])
def query_search():
    """ Returns ranked query results for a given query. Additionally, returns sorted list of categories for filtering.
        Input:
            query
        Output:
            'movies', query results
            'category list', list of categories
    """
    number_results = 100
    t0 = time.time()
    output = cache.get(request.get_json())
    if output:
        output['query_time'] = time.time() - t0
        return output

    query_params = preprocess_query_params(request.get_json().copy())
    query = query_params['query']
    search_phrase = query_params.get('search_phrase', False)
    if query is None or len(query) == 0:  # no query or the query consists only of stop words. Abort...
        return {'movies': [], 'category_list': [], 'query_time': time.time()-t0}

    query_id_results = ranked_retrieval(query_params, number_results, search_phrase)

    # Get quotes, quote_ids and movie_ids for the given query
    query_results = db.get_quotes_by_list_of_quote_ids(query_id_results)

    for i, dic_sentence in enumerate(query_results):
            dic_sentence['quote_id'] = dic_sentence.pop('_id')
            dic_sentence['full_quote'] = dic_sentence.pop('sentence')

    #Get Movie Details for movie_ids
    movie_ids = ([dic['movie_id'] for dic in query_results])
    movies = db.get_movies_by_list_of_ids(movie_ids)
    for dic_movie in movies:
        if dic_movie is not None and 'movie_id' not in dic_movie:  # movie_id may already be added if different quotes share the same movie!
            dic_movie['movie_id'] = dic_movie.pop('_id')

    #Merge Movie Details with Quotes
    query_results = merge_lists(query_results, movies, 'movie_id')

    #Create sorted list of all returned categories
    category_list = find_categories(query_results)
    t1 = time.time()
    print(f"Query took {t1-t0} s to process")

    if len(query_params['keywords']) > 0:
        query_results = filtering_keywords(query_results, query_params['keywords'])

    output = {'movies': query_results, 'category_list': category_list, 'query_time': t1-t0}
    cache.store(request.get_json(), output)
    return output
>>>>>>> master

@app.route('/movie_search', methods=['POST'])
def movie_search():
    """ Returns ranked query results for a given query. Additionally, returns sorted list of categories for filtering.
        Input:
            query
        Output:
            'movies', query results
            'category list', list of categories
    """
    number_results = 100
    t0 = time.time()
    output = cache.get(request.get_json())
    if output:
        output['query_time'] = time.time() - t0
        return output

    query_params = preprocess_query_params(request.get_json().copy())
    query = query_params['query']
    if query is None or len(query) == 0:  # no query or the query consists only of stop words. Abort...
        return {'movies': [], 'category_list': [], 'query_time': time.time()-t0}

    movie_id_results = ranked_movie_search(query_params, number_results)
    movies = db.get_movies_by_list_of_ids(movie_id_results)
    for dic_movie in movies:
        if dic_movie is not None:
            if '_id' in dic_movie:
                dic_movie['movie_id'] = dic_movie['_id']  # both movie_id and _id can be used

    #Create sorted list of all returned categories
    category_list = find_categories(movies)
    t1 = time.time()
    print(f"Query took {t1-t0} s to process")

    if len(query_params['keywords']) > 0:
        query_results = filtering_keywords(query_results, query_params['keywords'])

    output = {'movies': movies, 'category_list': category_list, 'query_time': t1-t0}
    cache.store(request.get_json(), output)
    return output

if __name__ == '__main__':
    app.run(debug=True, port=8000)
