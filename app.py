from flask import Flask, request

import json
import pymongo
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def main():
    client = connect_to_database()
    db = client["Spotify"]
    attribs = db["attributes"]
    count = attribs.count_documents({'danceability': {'$gt': 0.4}})
    return f"{count}"

@app.route('/query')
def query():
    client = connect_to_database()
    db = client["Spotify"]
    attribs = db["attributes"]
    q = request.args.get("q")

    out = f"query: {q}\n"
    for doc in attribs.find(json.loads(q)):
        print(doc)
        out += doc
    return out



def connect_to_database():
    CONNECTION_STRING = "mongodb://root:pass@localhost:27017/?authMechanism=DEFAULT"
    return MongoClient(CONNECTION_STRING)

def insert_csv_data(csv_path, db, collection_name):
    collection = db[collection_name]
    data = pd.read_csv(csv_path)
    collection.insert_many(data.to_dict(orient="records"))


if __name__ == "__main__":
    client = connect_to_database()
    db = client["Spotify"]
    print("importing data")
    insert_csv_data("Spotify_Song_Attributes.csv", db, "attributes")
    app.run(host="0.0.0.0", port=5000)
