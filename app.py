from flask import Flask

import pymongo
from pymongo import MongoClient

app = Flask(__name__)

CONNECTION_STRING = "mongodb://root:pass@localhost:27017/?authMechanism=DEFAULT"
client = MongoClient(CONNECTION_STRING)


@app.route('/')
def main():
    return f"{client}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
