import json
from bson import json_util
import pymongo
from flask import Flask, render_template_string, request, jsonify, redirect
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from template import HISTO, BARGRAPH, RAWDATA, PLAYLIST, GENRE

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

    # check if string is valid
    try:
        json.loads(query)
    except json.JSONDecodeError:
        return jsonify({'error', 'invalid query request'}), 400

    res = list(collection.find(json.loads(query)))
    return parse_json(res)

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

@app.route('/playlist', methods=['GET', 'POST'])
def genre_selection():
    if request.method == 'POST':
        # If a genre is selected, redirect to the playlist for that genre
        selected_genre = request.form.get('selected_genre')
        if selected_genre:
            return redirect(f'/playlist/{selected_genre}')
    
    # Query the MongoDB collection to get a list of unique genres
    pipeline = [
        {"$group": {"_id": "$genre"}},
        {"$sort": {"_id": 1}}
    ]
    genres = list(collection.aggregate(pipeline))	

    return render_template_string(GENRE, genres=genres)

@app.route('/playlist/<genre>')
def genre_playlist(genre):
    # Query the MongoDB collection for all songs with the specified genre
    query = {"genre": genre}
    songs_with_genre = list(collection.find(query))

    # Render the playlist template with the specified genre and songs
    return render_template_string(PLAYLIST, genre=genre, data=songs_with_genre)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
