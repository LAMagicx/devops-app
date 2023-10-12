from flask import Flask, request, jsonify
from bson import json_util
import pymongo, json
import pandas as pd
import os
from pymongo import MongoClient


def insert_csv_data(csv_path, db, collection_name):
    collection = db[collection_name]
    data = pd.read_csv(csv_path)
    collection.insert_many(data.to_dict(orient="records"))

def parse_json(data):
    return json.loads(json_util.dumps(data))


app = Flask(__name__)

client = MongoClient(host="mongodb",
                     port=27018,
                     username="root",
                     password="pass")
print("Mongo Client Loaded")
db = client["spotifyDB"]
if "spotifyDB" not in client.list_database_names():
    print("Spotify database is not loaded")
    print("Loading spotify data")
    insert_csv_data("Spotify_small.csv", db, "attributes")

attribs = db["attributes"]

@app.route('/')
def main():
    return f"{client}"

@app.route('/query')
def query_mongo():
    query = request.args.get("q")

    # check if string is valid
    try:
        json.loads(query)
    except json.JSONDecodeError:
        return jsonify({'error', 'invalid query request'}), 400

    res = list(attribs.find(json.loads(query)))
    return parse_json(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
