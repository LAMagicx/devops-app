from flask import Flask, render_template
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# Connect to your MongoDB instance
client = MongoClient("mongodb://root:pass@27017:27017/spotifydb")
db = client['spotifydb'] # Replace with your database name
collection = db['spot']  # Replace with your collection name
data = collection.find({})

@app.route('/')
def main():
    res = "Hello there..<br>"
    res += "Connected to MongoDB: " + str(client) + "<br>"
    res += "Selected database: " + str(db) + "<br>"
    res += "Selected collection: " + str(collection)+"<br><<"   
    return res

@app.route('/dataview')
def view_data():
    # Retrieve data from MongoDB collection
    data = collection.find({})
    
    # Render the template with the retrieved data
    return render_template('dataview.html', data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
