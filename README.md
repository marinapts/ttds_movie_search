# TTDS Movie Search IR Project 2020

This is a group project for the course [TTDS](https://www.inf.ed.ac.uk/teaching/courses/tts/) (Text Technologies for Data Science)
at the University of Edinburgh.
We received the "Best Project Award" for the term 2019-2020 and the webpage will be soon hosted in one of the
University's servers.

Currently it can be accessed from this link: http://167.71.139.222

## Summary

It is a webpage that finds quotes and quote details for popular movies and TV shows. Given a query, it returns the most
relevant quotes, along with the corresponding movie details. The collection of documents contains 77,584,425 quotes
from 218,000 movies and TV shows. It uses a multi-level inverted index occupying 21.7GB on disk. The ranking
algorithm uses BM25 and logarithmic popularity weighting for phrase search. Instead of quotes, the
website can also perform a second search for full movies using weighted TFIDF algorithm. It also contains advanced
search features, such as filtering by year, actors and keywords, and it includes genre filtering and query completion.


The project consists of 4 basic parts:
* data_collection
* ir_eval: IR indexing and ranking
* gui: gui build with React
* api: api built with Flask

Read the README files under each project for more details.

## Installation
You need to have Python 3 installed.

Create a local environment and install the requirements:
```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
pip install -e .
```


### Run the front-end
```bash
cd gui
npm start
```
If the folder `node_modules` doesn't exist under the gui folder, run ```npm install``` first and then ```npm start```


### Run the back-end
```bash
cd api
./run.sh
```

### Testing
Add your tests to the `tests/` folder. The file names should start with `test_`. Each test method should also start with `test_`. See `tests/test_phrase_search.py` for an example. Execute the following command to run tests:
```bash
python -m unittest discover -p test*.py
```
