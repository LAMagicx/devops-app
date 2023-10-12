import csv, json
from bson import json_util
import pymongo
from flask import Flask, render_template_string, request, jsonify, render_template
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np
import plotly.express as px
from pymongo import MongoClient
from template import HISTO, BARGRAPH, RAWDATA
from sklearn.decomposition import PCA

app = Flask(__name__)

def insert_csv_data(csv_path, db, collection_name):
    collection = db[collection_name]
    data = pd.read_csv(csv_path)
    collection.insert_many(data.to_dict(orient="records"))

def parse_json(data):
    return json.loads(json_util.dumps(data))

def calculate_song_distance(s1, s2):
    numerical_features = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "valence", "tempo"]

    return np.linalg.norm(s1[numerical_features].values, s2[numerical_features].values)


client = pymongo.MongoClient("mongodb://root:pass@localhost:27018")
print("Mongo Client Loaded")
db = client["spotifyDB"]
if "spotifyDB" not in client.list_database_names():
    print("Spotify database is not loaded")
    print("Loading spotify data")
    insert_csv_data("Spotify_small.csv", db, "attributes")

collection = db["attributes"]
print("Client finished loading")

@app.route('/')
def raw():
    # Extract all data from the MongoDB collection
    all_documents = list(collection.find().limit(20))

    return render_template_string(RAWDATA, data=all_documents)

@app.route('/genre-bar-graph')
def genre_bar_graph():
    # Query data from the MongoDB collection and group by genre
    pipeline = [
        {"$match": {"genre": {"$ne": "no value"}}},
        {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    cursor = collection.aggregate(pipeline)
    data = list(cursor)
    # Extract the genre and count information
    genres = [entry['_id'] for entry in data]
    counts = [entry['count'] for entry in data]
    # Create a bar graph using Plotly
    fig = go.Figure(data=[go.Bar(x=genres, y=counts)])
    fig.update_layout(title="Number of Songs by Genre", xaxis_title="Genre", yaxis_title="Count")

    # Convert the Plotly graph to HTML for rendering
    genre_bar_graph_html = pio.to_html(fig)

    return render_template_string(BARGRAPH, genre_bar_graph=genre_bar_graph_html)

@app.route('/query')
def query_mongo():
    query = request.args.get("q")
    search = request.args.get("s")

    # check if string is valid
    try:
        json.loads(query)
    except json.JSONDecodeError:
        return jsonify({'error', 'invalid query request'}), 400

    find_res = list(collection.find(json.loads(query)))
    print(find_res)
    if search:
        df = pd.DataFrame(find_res).dropna()
        title_res = df[df["trackName"].apply(str.lower).str.contains(search)]
        artist_res = df[df["artistName"].apply(str.lower).str.contains(search)]
        search_results = pd.concat([title_res, artist_res]).drop_duplicates()

        return parse_json(search_results.to_dict(orient="records"))
    else:
        return parse_json(find_res)

@app.route('/histograms')
def histograms():
    # Query data from the MongoDB collection
    cursor = collection.find({}, {"_id": 0, "danceability": 1, "energy": 1, "valence": 1})
    data = list(cursor)

    # Create a DataFrame from the MongoDB data
    df = pd.DataFrame(data)

    # Create histograms using Plotly
    danceability_histogram = px.histogram(df, x="danceability", title="Danceability Histogram")
    energy_histogram = px.histogram(df, x="energy", title="Energy Histogram")
    valence_histogram = px.histogram(df, x="valence", title="Valence Histogram")

    # Convert the Plotly plots to HTML for rendering
    danceability_html = danceability_histogram.to_html()
    energy_html = energy_histogram.to_html()
    valence_html = valence_histogram.to_html()

    return render_template_string(HISTO, danceability=danceability_html, energy=energy_html, valence=valence_html)

@app.route('/dist')
def distances():
    search_term = request.args.get('q')

    df = pd.DataFrame(list(collection.find())).dropna()
    
    if search_term:
        result = f"Search results for: {search_term}"
        search_results = df["trackName"].apply(str.lower).str.contains(search_term.lower())
    else:
        result = None

    return render_template('search.html', result=result)

@app.route('/scatter')
def analyse():
    # pca analysis of songs
    df = pd.DataFrame(list(collection.find())).dropna()
    numerical_features = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "valence", "tempo"]

    pca = PCA(n_components=3)
    data = pca.fit_transform(df[numerical_features])

    df["X"] = data[:, 0]
    df["Y"] = data[:, 1]
    df["Z"] = data[:, 2]

    df["name"] = df["trackName"] + " - " + df["artistName"]

    return px.scatter_3d(df, x="X", y="Y", z="Z", color="danceability", hover_name="name").to_html()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
