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

### Testing
Add your tests to the `tests/` folder. The file names should start with `test_`. Each test method should also start with `test_`. See `tests/test_phrase_search.py` for an example. Execute the following command to run tests:
```bash
python -m unittest discover -p test*.py
```

## Deploying on DigitalOcean
### First Time Setup
Install Miniconda3 on DigitalOcean, create and activate an environment called `ttds-prod` (Python 3.6):
```bash
conda create -n ttds-prod python=3.6
conda activate ttds-prod
```

Install production requirements: `pip install -r requirements-prod.txt`. Note, uWSGI may fail to install. In that case, install it via conda:
```bash
conda install -c conda-forge uwsgi
```

Copy file `ttds.service` to `/etc/systemd/system/` (sudo privilleges required). Run:
```bash
sudo systemctl start ttds
sudo systemctl enable ttds
```

To check the status, run: `sudo systemctl status ttds`. The app should now be available to access via http://DIGITAL_OCEAN_DROPLET_IP:5000 (or http://DIGITAL_OCEAN_DROPLET_IP if you have set up port 80 to redirect to 5000).

### Serve React build from Flask
Go to the gui folder and create the minified React build:
```bash
cd gui
npm run build
```

This will create a folder `build` which contains the minified JS and CSS files that are ready for production. The output should include something like this:
```
File sizes after gzip:

  113.27 KB (+14.78 KB)  build/static/js/2.e5f334b4.chunk.js
  4.78 KB (+295 B)       build/static/js/main.ffeeed21.chunk.js
  821 B (+5 B)           build/static/css/main.b73ac9ac.chunk.css
  768 B                  build/static/js/runtime-main.7f72db5d.js
```

We only need these files and build/static/index.html.

The React build will be served from the static folder in api. Delete any old js and css files under api/static (if any) and copy the generated js, css and index.html into api/static.
```bash
rm api/static/js/*
rm api/static/css/*

cp gui/build/static/js/2.e5f334b4.chunk.js api/static/js/
cp gui/build/static/js/main.ffeeed21.chunk.js api/static/js/
cp gui/build/static/js/runtime-main.7f72db5d.js api/static/js/
cp gui/build/static/css/main.b73ac9ac.chunk.css api/static/css/
cp gui/build/static/index.html api/static/
```

Next, replace the js and css files in `templates/template.html` with the ones above, so `filename="js/2.f10b8685.chunk.js"` should be `filename="js/2.e5f334b4.chunk.js"` and so on.


### How to Restart with Code Changes
Once the service is up and running, you can update the app simply by pulling a new version from git and running `./restart_on_digital_ocean.sh` from the repository root folder.
