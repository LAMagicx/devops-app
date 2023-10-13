import requests
import json
from bson import json_util
import pymongo
from flask import Flask, render_template_string, request, jsonify, redirect
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np
import plotly.express as px
from pymongo import MongoClient
from template import HISTO, BARGRAPH, RAWDATA, PLAYLIST, GENRE, SEARCHRESULTS, NORESULT
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

@app.route('/query', methods=['GET', 'POST'])
def query_mongo():
    query = request.args.get("search_query")
    df = pd.DataFrame(list(collection.find()))

    if query:
        # Apply a filter if a search query is provided
        filtered_data = df[df['trackName'].str.contains(query, case=False)]
        if filtered_data.empty:
            # If the filtered data is empty, render a specific template for no results
            return render_template_string(NORESULT)
    else:
        # If no search query, show all data
        filtered_data = df
    
    return render_template_string(SEARCHRESULTS, data=filtered_data.to_dict('records'), search_query=query)

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


@app.route("/1406")
def sorting_db():
	Key = request.args.get("key")

	"""Cette fonction trie les collones dans l'ordre décroissant si possible."""
	# print(f"Key: {key}")  # Ajouter du débogage pour voir la clé

	keys = ['msPlayed', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'acousticness', 'liveness', 'valence', 'tempo', 'duration_ms']

	if Key in keys:
		data = list(collection.find().sort(Key, -1).limit(20))
		return render_template_string(RAWDATA, data=data)
	else:
		return "key not found"

# ################### Jira #######################""
def get_jira_credentials(username):
	with open('config.json', 'r') as config_file:
		config_data = json.load(config_file)
	
	for user in config_data['users']:
		if user['username'] == username:
			return user['api_token']
	
	return None

# Your Jira API information
JIRA_URL = 'https://rawdata.atlassian.net/rest/api/2/issue'
JIRA_USERNAME = 'melol1812222@gmail.com'

@app.route('/create_jira_issue', methods=['GET','POST'])
def create_jira_issue():
	api_token = get_jira_credentials(JIRA_USERNAME)

	if api_token is None:
		return jsonify({'error': 'User not found or missing credentials'}), 401

	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json'
	}

	auth = (JIRA_USERNAME, api_token)

	# Data for creating a Jira issue
	issue_data = {
		"fields": {
			"project": {
				"key": "KAN"
			},
			"summary": "New Issue",
			"description": "This is a test issue created via the API.",
		}
	}
	data_json = json.dumps(issue_data)

	# Create the issue
	response = requests.post(JIRA_URL, headers=headers, auth=auth, data=data_json)

	if response.status_code == 200 or response.status_code == 201:
		return jsonify(response.json())  # Return the JSON response from Jira
	else:
		return jsonify({'error': 'Failed to retrieve Jira issues'}), response.status_code

@app.route('/get_jira_issues')
def get_jira_issues():
	# username = request.args.get('username')  
	API_TOKEN = get_jira_credentials(JIRA_USERNAME)

	if API_TOKEN is None:
		return jsonify({'error': 'User not found or missing credentials'}), 401

	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json'
	}

	auth = (JIRA_USERNAME, API_TOKEN)

	# Example GET request to retrieve issues
	response = requests.get(f'{JIRA_URL}/search', headers=headers, auth=auth)

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
