from flask import Flask, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
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
    with open('movies.json') as movies:
        movies_dict = json.load(movies)

    return json.dumps({'movies': movies_dict[:20]})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
