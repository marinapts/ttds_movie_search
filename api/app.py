from flask import Flask, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from db.DB import get_db_instance
import json

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


@app.route('/query_search', methods=['POST'])
def query_search():
    query_params = request.get_json()

    # @TODO: Get movies for the given query
    movies = db.get_movies_by_list_of_ids(['tt0111161',
                                           'tt0068646',
                                           'tt0468569',
                                           'tt0071562',
                                           'tt0167260',
                                           'tt0110912',
                                           'tt0108052',
                                           'tt0050083',
                                           'tt1375666',
                                           'tt0137523',
                                           'tt0120737',
                                           'tt0109830',
                                           'tt0060196',
                                           'tt7286456',
                                           'tt0167261',
                                           'tt0133093',
                                           'tt0099685',
                                           'tt0080684',
                                           'tt0073486',
                                           'tt0056058'])

    return json.dumps({'movies': movies})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
