#!/bin/bash

# environment variables
export FLASK_ENV=production
source .env/bin/activate
flask run
