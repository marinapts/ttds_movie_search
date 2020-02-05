# TTDS Movie Search IR Project 2020

The project consists of 4 basic parts:
* data_collection
* ir_eval: IR indexing and ranking
* gui: gui build with React
* api: api built with Flask

Read the README files under each project for more details.

## Installation

Create a local environment and install the requirements:
```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
pip install -e .
```


### Run the front-end
```
cd gui
npm start
```
If node_modules doesn't exist, run ```npm install``` first and then ```npm start```


### Run the back-end
```
cd api
./run.sh
```

