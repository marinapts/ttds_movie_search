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
    fake_movies = [
        {
            'id': 1,
            'title': 'Movie Title 1',
            'description': 'Movie Description 1',
            'info': 'Movie Info 1',
        },
        {
            'id': 2,
            'title': 'Movie Title 2',
            'description': 'Movie Description 2',
            'info': 'Movie Info 2',
        },
        {
            'id': 3,
            'title': 'Movie Title 3',
            'description': 'Movie Description 3',
            'info': 'Movie Info 3',
        },
        {
            'id': 4,
            'title': 'Movie Title 4',
            'description': 'Movie Description 4',
            'info': 'Movie Info 4',
        }
    ]
    return json.dumps({'movies': fake_movies})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
