from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/test')
def testing():
    return 'Hey ttds team, routes seem to be working :)'


@app.route('/query_search', methods=['POST'])
def query_search():
    content = request.get_json()
    query = content['query']

    # @TODO: Get movies for the given query
    with open('movies.json') as movies:
        movies_dict = json.load(movies)

    return json.dumps({'movies': movies_dict})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
