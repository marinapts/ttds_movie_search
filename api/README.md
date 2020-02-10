# REST API using Flask

You need to have Python 3 installed.


## Install dependencies
The first time you clone the project, run `python3 -m venv .env` which creates a virtual environment
using the command venv and stores all the dependencies under the folder .env.

Run the following to ensure that all of us are using the same versions of Python packages.
Activate the virtual environment on the project's folder and then install the packages from requirements.txt

```bash
source ./.env/bin/activate
pip install -r requirements.txt
```

## Run the app
Run the app by calling the shell script `./run.sh` or `bash run.sh`, which serves the api on **localhost:5000**

The routes **/** and **/test** are accessible and return the test messages. These will be soon modified, I just wanted
to check that it's running.

## Deployment
The following commands should be run on the root folder of the repository:
* Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
* Login to your Heroku account: `heroku login`
* Add Heroku remote repository: `heroku git:remote -a ttds-movie-search`
* The app must be at the root of a repository pushed to Heroku. To deploy, run the following command: `git subtree push --prefix api heroku master`


### Notes
The gui and api parts can communicate for development, but not yet for production.

### Developing database methods
Add a new abstract method to `db/DBInterface` and then implement that method in the database class we are going to use (for now `db/ShelveDB`).