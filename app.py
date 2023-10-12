import csv
import pymongo
from flask import Flask, render_template_string, request
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import plotly.express as px
from template import HISTO, BARGRAPH, RAWDATA
"""

"""
app = Flask(__name__)

# Initialize a connection to the MongoDB database
mongo_client = pymongo.MongoClient("mongodb://root:pass@localhost:27018")
db = mongo_client["my_database"]
collection = db["spotify_data"]

# Read data from CSV file and insert it into the MongoDB collection
with open('Spotify_Song_Attributes.csv', 'r') as file:
	csv_reader = csv.DictReader(file)
	for row in csv_reader:
		collection.insert_one(row)

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

    return render_template_string(HISTO, danceability=danceability_html,
                           energy=energy_html, valence=valence_html)

if __name__ == '__main__':
	app.run(debug=True, port=5000)