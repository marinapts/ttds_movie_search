from flask import Flask, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from db.DB import get_db_instance
import json
#from preprocessing_api import preprocess
from ir_eval.ranking.main import ranked_retrieval
import re
import time
from ir_eval.preprocessing import preprocess

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

@app.route('/query_search', methods=['POST'])
def query_search():
    """ Returns ranked query results for a given query. Additionally, returns sorted list of categories for filtering.
        Input:
            query
        Output:
            'movies', query results
            'category list', list of categories
    """
    batch_size = 20
    number_results = 100
    query_params = request.get_json()

    query = query_params['query']

    filter_title = query_params['movie_title']
    #filter_title = ''
    filter_actor = query_params['actor']
    #filter_actor = ''
    filter_keywords = query_params['keywords']
    #filter_keywords = ''
    filter_years = query_params['year']

    #filter_years = '1970-2010'

    t0 = time.time()
    # Get search input 'query' and perform tokenisation etc
    query = preprocess(query)
    query_params['query'] = query

    # @Todo: send query to ranking function and receive quote ids
    query_id_results = ranked_retrieval(query_params, db, batch_size, number_results)

    # Get quotes, quote_ids and movie_ids for the given query
    query_results = db.get_quotes_by_list_of_quote_ids(query_id_results)[0:100000]

    # query_results = db.get_quotes_by_list_of_quote_ids([234,
    #                                                     234234,
    #                                                     1151,
    #                                                     15,
    #                                                     488483,
    #                                                     3453222])

    # to_delete = []
    # for i, dic_sentence in enumerate(query_results):
    #     if len(dic_sentence['sentence']) > 1000:
    #         to_delete.append(i)

    # for i in sorted(to_delete, reverse=True):
    #     del query_results[i]

    for i, dic_sentence in enumerate(query_results):
            dic_sentence['quote_id'] = dic_sentence.pop('_id')
            dic_sentence['full_quote'] = dic_sentence.pop('sentence')

    #Get Movie Details for movie_ids
    movie_ids = ([dic['movie_id'] for dic in query_results])
    movies = db.get_movies_by_list_of_ids(movie_ids)
    for dic_movie in movies:
        if dic_movie is not None:
            dic_movie['movie_id'] = dic_movie.pop('_id')

    #Merge Movie Details with Quotes
    query_results = merge_lists(query_results, movies, 'movie_id')

    # #Filtering
    # if filter_title != '':
    #     query_results = filtering_title(query_results, filter_title)

    # # @TODO: Function to filter by actors

    # if filter_years != '':
    #     query_results = filtering_years(query_results, filter_years)

    # if filter_keywords != '':
    #     query_results = filtering_keywords(query_results, filter_keywords)

    #Create sorted list of all returned categories
    category_list = find_categories(query_results)
    t1 = time.time()
    print(t1-t0)

    return json.dumps({'movies': query_results, 'category_list': category_list})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
