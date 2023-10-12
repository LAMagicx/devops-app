import csv
import pymongo
from flask import Flask, render_template_string, request
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import plotly.express as px
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

HISTO = '''<!DOCTYPE html>
<html>
<head>
    <title>Histograms</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Histograms</h1>
    <div id="danceability_histogram"></div>
    <div id="energy_histogram"></div>
    <div id="valence_histogram"></div>
    <a href="/"><button>Back to Raw Data</button></a>
    <a href="/genre-bar-graph"><button>View Genre Bar Graph</button></a>

    <script>
        // Use JavaScript to display Plotly plots in the placeholders
        var danceability_plot = {{ danceability | safe }};
        var energy_plot = {{ energy | safe }};
        var valence_plot = {{ valence | safe }};
        
        document.getElementById('danceability_histogram').innerHTML = danceability_plot;
        document.getElementById('energy_histogram').innerHTML = energy_plot;
        document.getElementById('valence_histogram').innerHTML = valence_plot;
    </script>
</body>
</html>

'''

BARGRAPH = '''
<!DOCTYPE html>
<html>
<head>
    <title>Genre Bar Graph</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Genre Bar Graph</h1>
    <div id="genre_bar_graph"></div>
    <a href="/"><button>Back to Raw Data</button></a>
    <a href="/histograms"><button>View Histograms</button></a>
    
    <script>
        // Use JavaScript to display the Plotly bar graph
        var genre_bar_graph_plot = {{ genre_bar_graph | safe }};
        document.getElementById('genre_bar_graph').innerHTML = genre_bar_graph_plot;
    </script>
</body>
</html>
'''

RAWDATA = '''
<!DOCTYPE html>
<html>
<head>
    <title>Raw Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }
        h1 {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #333;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        #histogram-button {
            text-align: center;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h1>Raw Data</h1>
    <div id="histogram-button">
    	<a href="/histograms"><button>Switch to Histogram View</button></a>
    	<a href="/genre-bar-graph"><button>View Genre Bar Graph</button></a> <!-- New button for the bar graph page -->
	</div>
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