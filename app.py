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

@app.route('/histograms')
def histograms():
    # Sample data for demonstration
    data = {
        "danceability": [0.7, 0.8, 0.6, 0.9, 0.5],
        "energy": [0.6, 0.7, 0.8, 0.5, 0.4],
        "valence": [0.8, 0.7, 0.9, 0.6, 0.5],
    }

    df = pd.DataFrame(data)

    # Create histograms using Plotly
    danceability_histogram = px.histogram(df, x="danceability")
    energy_histogram = px.histogram(df, x="energy")
    valence_histogram = px.histogram(df, x="valence")

    # You can also customize the layout of the histograms
    danceability_histogram.update_layout(title_text="Danceability Histogram")
    energy_histogram.update_layout(title_text="Energy Histogram")
    valence_histogram.update_layout(title_text="Valence Histogram")

    return render_template_string(HISTO, danceability=danceability_histogram.to_html(),
                           energy=energy_histogram.to_html(), valence=valence_histogram.to_html())

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