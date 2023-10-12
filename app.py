from flask import Flask, request
import json
import pymongo
import pandas as pd
from pymongo import MongoClient


def insert_csv_data(csv_path, db, collection_name):
    collection = db[collection_name]
    data = pd.read_csv(csv_path)
    collection.insert_many(data.to_dict(orient="records"))


app = Flask(__name__)

CONNECTION_STRING = "mongodb://root:pass@localhost:27017/?authMechanism=DEFAULT"
client = MongoClient(CONNECTION_STRING)
db = client["Spotify"]
insert_csv_data("Spotify_Song_Attributes.csv", db, "attributes")

@app.route('/')
def main():
    db = client["Spotify"]
    attribs = db["attributes"]
    count = attribs.count_documents({'danceability': {'$gt': 0.4}})
    return f"{count}"

@app.route('/query')
def query():
    attribs = db["attributes"]
    q = request.args.get("q")

    out = f"query: {q}\n"
    for doc in attribs.find(json.loads(q)):
        print(doc)
        out += doc
    return out


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
