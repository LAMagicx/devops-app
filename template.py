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
    <input type="text" id="searchInput" placeholder="Saisir le nom dune collonne">
    <button onclick="rechercherAvecCle()">Rechercher</button>

    <script>
        function rechercherAvecCle() {
            // Récupérer la valeur saisie par l'utilisateur
            var cle = document.getElementById("searchInput").value;
            
            // Construire l'URL de recherche
            var urlDeRecherche = "/1406?key=" + cle;

            // Rediriger la fenêtre vers l'URL de recherche
            window.location.href = urlDeRecherche;
        }
    </script>

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