from flask import Flask
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
    attribs = db["attributes"]
    count = attribs.count_documents({'danceability': {'$gt': 0.4}})
    return f"{count}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
