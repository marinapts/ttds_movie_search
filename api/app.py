from flask import Flask, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from db.DB import get_db_instance
import json
from preprocessing_api import preprocess

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

def merge_lists(l1, l2, primary_key, secondary_key):
    merged = l1
    for n, item1 in enumerate(l1):
        for item2 in l2:
            if item1[secondary_key] == item2[secondary_key]:
                merged[n].update(item2)
    return merged

@app.route('/query_search', methods=['POST'])
def query_search():
    query_params = request.get_json()

    query = query_params['query']

    #@TODO: Get search input 'query' and perform tokenisation etc 
    query = preprocess(query)

    #@TODO: Get quotes, quote_ids and movie_ids for the given query
    query_results = [
        {
              'quote_id': 1,
              'full_quote': 'This is a quote 1',
              'movie_id': 'tt0111161'
        },
        {
              'quote_id': 2,
              'full_quote': 'This is a quote 2',
              'movie_id': 'tt0068646'
        },
        {
              'quote_id': 3,
              'full_quote': 'This is a quote 3',
              'movie_id': 'tt0468569'
        },
        {
              'quote_id': 4,
              'full_quote': 'This is a quote 4',
              'movie_id': 'tt0167260'
        },
        {
              'quote_id': 5,
              'full_quote': 'This is a quote 5',
              'movie_id': 'tt0167260'
        },
    ]


    #Get Movie Details for movie_ids
    movie_ids = ([dic['movie_id'] for dic in query_results])
    movies = db.get_movies_by_list_of_ids(movie_ids)
    for dic_movie in movies:
        dic_movie['movie_id'] = dic_movie.pop('id')

    #Merge Movie Details with Quotes
    query_results = merge_lists(query_results, movies, 'quote_id', 'movie_id')

    #return json.dumps({'movies': movies})
    return json.dumps({'movies': query_results})

if __name__ == '__main__':
    app.run(debug=True, port=8000)

