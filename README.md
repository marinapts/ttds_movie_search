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

Once the service is up and running, you can update the app simply by pulling a new version from git and running `./restart_on_digital_ocean.sh` from the repository root folder.
