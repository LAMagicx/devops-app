from flask import Flask

import pymongo
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def main():
    return "Hello there.."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
