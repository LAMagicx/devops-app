from flask import Flask

import pymongo
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def main():
    return "Hello there.."

def get_database():
    CONNECTION_STRING = "mongodb://localhost:27017/devops-app-DB"
    client = MongoClient(CONNECTION_STRING)
    return client['devops-app-DB']

def insert_data(collection_name):
    item_1 = {
    "_id" : "U1IT00001",
    "item_name" : "Blender",
    "max_discount" : "10%",
    "batch_number" : "RR450020FRG",
    "price" : 340,
    "category" : "kitchen appliance"
    }

    item_2 = {
    "_id" : "U1IT00002",
    "item_name" : "Egg",
    "category" : "food",
    "quantity" : 12,
    "price" : 36,
    "item_description" : "brown country eggs"
    }
    collection_name.insert_many([item_1,item_2])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    dbname = get_database()
    collection_name = dbname["test-collection"]
    insert_data(collection_name)