import csv
import pymongo
from flask import Flask, render_template_string, render_template, request
import plotly.graph_objects as go
import plotly.io as pio
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

@app.route('/raw')
def raw():
    # Extract all data from the MongoDB collection
    all_documents = list(collection.find())

    return render_template_string(RAWDATA, data=all_documents)

@app.route('/')
def index():
	search_letter = request.args.get('search', '').upper()
	if search_letter:
		# Regex to filter artists by the first letter of their name
		query = {'artistName': {'$regex': f'^{search_letter}'}}
		projection = {'artistName': 1, '_id': 0}
		artists = collection.find(query, projection)

	else:
		artists = collection.find({}, {'artistName': 1, '_id': 0})
	artists_list = list(artists)
	return render_template_string(TEMPLATE, artists=artists_list)

##################################################      Sort by criteria   ##############
@app.route('/sort/<criteria>')
def sort(criteria):
    """
    Route to sort and display artists based on a given criteria.
    
    Parameters:
    criteria (str): The field by which to sort the artists. 
                    Valid values are 'streams', 'released_year', and 'danceability_%'.
    
    Returns:
    str: Rendered HTML template as a string.
    """
    if criteria not in ['streams', 'released_year', 'danceability_%']:
        return "Invalid criteria", 400  # retourne une erreur si le critère n'est pas valide
    sort_criteria = [(criteria, -1)]  # -1 pour le tri descendant
    artists = collection.find({}, {'artistName': 1, '_id': 0}).sort(
        sort_criteria
    )  # Split long line into two lines
    return render_template_string(TEMPLATE, artists=artists)

##################################################      Data Vizualisation  ###############
@app.route('/visualize/<key>')
def visualize(key):
    """Cette fonction génère un histogramme basé sur la clé donnée."""
    # print(f"Key: {key}")  # Ajouter du débogage pour voir la clé
    data = db.spotify.find({}, {key: 1, 'artistName': 1, '_id': 0})
    values = []
    artist_names = []
    for item in data:
        if key in item and 'artistName' in item:
            values.append(item[key])
            artist_names.append(item['artistName'])
    hover_texts = [
        f"{artist_name}<br>{key}: {value}" for artist_name, value in zip(artist_names, values)
    ]

    trace = go.Histogram(
        x=values,
        text=hover_texts,  # Set hover text
        hoverinfo='text'  # Only show custom hover text
    )
    fig = go.Figure(data=trace)
    fig_div = pio.to_html(fig, full_html=False)
    return render_template_string(TEMPLATE, fig_div=fig_div)

TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
	<!-- Required meta tags -->
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	<!-- Bootstrap CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">

	<!-- Dark Theme Styles -->
	<style>
		body {
			background-color: #343a40;
			color: #ffffff;
		}
		.container {
			background-color: #454d55;
			border-radius: 10px;
			padding: 20px;
		}
		.list-group-item {
			background-color: #454d55;
			color: #ffffff;  <!-- Ajout de cette règle pour définir la couleur du texte en blanc -->
		}
	</style>

	<title>Spotify Artists</title>
  </head>
  <body>
	<div class="container">
	  <h1 class="mt-5">Ma p'tite biblio spotify</h1>
	   <div class="mt-3 mb-3">
	   <a href="/visualize/tempo" class="btn btn-primary mb-3">Visualiser par indicateur "tempo"</a><br>
		<a href="/visualize/msPlayed" class="btn btn-primary mb-3">Visualiser par indicateur "Most Played"</a><br>
		<a href="/visualize/energy" class="btn btn-primary mb-3">Visualiser par indicateur "energy"</a><br>
		Sort by: 
			<a href="/sort/streams">Streams</a> | 
			<a href="/sort/released_year">Year</a> | 
			<a href="/sort/danceability_%">Danceability</a>
		</div>
		<div class="mt-4 mb-4">
			<!-- Alphabet links -->
			{% for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' %}
				<a href="/?search={{ letter }}">{{ letter }}</a>
			{% endfor %}
		</div>
		<!-- Add this div to display the Plotly graph -->
		<div class="mt-4">
			{{ fig_div | safe }}
		</div>
		
		</div>
		<ul class="list-group mt-3">
			{% for artist in artists %}
				<li class="list-group-item">{{ artist['artistName'] }}</li>
			{% endfor %}
		</ul>
	</div>

	<!-- Optional JavaScript; choose one of the two! -->

	<!-- Option 1: Bootstrap Bundle with Popper -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
'''


RAWDATA = '''
<!DOCTYPE html>
<html>
<head>
    <title>Raw Data</title>
</head>
<body>
    <h1>Raw Data</h1>
    <table>
        <tr>
            {% for key, _ in data[0].items() %}
                <th>{{ key }}</th>
            {% endfor %}
        </tr>
        {% for document in data %}
            <tr>
                {% for key, value in document.items() %}
                    <td>{{ value }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </table>
</body>
</html>

'''

if __name__ == '__main__':
	app.run(debug=True, port=5000)