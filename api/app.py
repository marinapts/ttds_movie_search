from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/test")
def testing():
    return "Hey ttds team, routes seem to be working :)"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
