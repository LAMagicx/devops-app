from flask import Flask, request, jsonify
from bson import json_util

import pymongo, json
import pandas as pd
from pymongo import MongoClient

def parse_json(data):
    return json.loads(json_util.dumps(data))


app = Flask(__name__)


CONNECTION_STRING = "mongodb://root:pass@localhost:27017/?authMechanism=DEFAULT"
client = MongoClient(CONNECTION_STRING)
db = client["Spotify"]
attribs = db["attributes"]

@app.route('/')
def main():
    count = attribs.count_documents({'danceability': {'$gt': 0.4}})
    return f"c:{count}"

@app.route('/query')
def query_mongo():
    query = request.args.get("q")
    try:
        query_dict = eval(query)
    except Exception as e:
        return jsonify({'error', 'invalid query'}), 400
    try:
        print(query)
        print(query_dict)
        res = list(attribs.find(query_dict))
        return parse_json(res), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def insert_csv_data(csv_path, db, collection_name):
    collection = db[collection_name]
    data = pd.read_csv(csv_path)
    collection.insert_many(data.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
