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
    <a href="/"><button>Back to Home</button></a>
    <a href="/genre-bar-graph"><button>View Genre Bar Graph</button></a>

    <script>
        // Use JavaScript to display Plotly plots in the placeholders
        var danceability_plot = {{ danceability | safe }}
		{{ energy | safe }}
        {{ valence | safe }};
        
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
    <a href="/"><button>Back to Home</button></a>
    <a href="/histograms"><button>View Histograms</button></a>
    
    <script>
        // Use JavaScript to display the Plotly bar graph
        var genre_bar_graph_plot = {{ genre_bar_graph | safe }}
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
    <input type="text" id="searchInput" placeholder="Saisir le nom dune colonne">
    <button onclick="rechercherAvecCle()">SORT</button>

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
    	<a href="/genre-bar-graph"><button>View Genre Bar Graph</button></a>
    	<a href="/playlist"><button>Get a playlist of your chosen genre</button></a>
    	<a href="/scatter"><button>SCATTER PLOT OF SONGS</button></a>
	</div>
    <!--- Search bar --->
    <form action="/query" onsubmit="searchSongs();">
        <label for="search_query">Search:</label>
        <input type="text" id="search_query" name="search_query">
        <input type="submit" value="Submit">
    </form>

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

SEARCHRESULTS = '''
<!DOCTYPE html>
<html>
<head>
    <title>Search Results</title>
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
    <h1>Search Results</h1>
    <div id="histogram-button">
        <a href="/histograms"><button>Switch to Histogram View</button></a>
        <a href="/genre-bar-graph"><button>View Genre Bar Graph</button></a> <!-- New button for the bar graph page -->
        <a href="/"><button>Back to Raw Data</button></a>
    </div>
<!--- Search bar --->
    <form action="/query" onsubmit="searchSongs();">
        <label for="search_query">Search:</label>
        <input type="text" id="search_query" name="search_query">
        <input type="submit" value="Submit">
    </form>
    <script>
    console.log(data.toString())
    </script>
    {% if data.empty %}
        <p>No results found.</p>
    {% else %}
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
    {% endif %}

    <script>
        function searchSongs() {
            const searchQuery = document.getElementById('search_query').value;
            const table = document.querySelector('table');
            const rows = table.querySelectorAll('tr');

            for (let i = 1; i < rows.length; i++) {  // Start from 1 to skip the header row
                const trackName = rows[i].querySelector('td:first-child').textContent.toLowerCase();
                if (trackName.includes(searchQuery.toLowerCase())) {
                    rows[i].style.display = 'table-row';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        }
    </script>
    <div id="search-results">
        <!-- Search results will be displayed here -->
    </div>
    
</body>
</html>
'''

PLAYLIST = '''
<!DOCTYPE html>
<html>
<head>
    <title>Playlist</title>
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
    <h1>Playlist for Genre: {{ genre }}</h1>
    <div id="histogram-button">
        <a href="/histograms"><button>Switch to Histogram View</button></a>
        <a href="/genre-bar-graph"><button>View Genre Bar Graph</button></a>
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

GENRE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Choose Genre</title>
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
        form {
            text-align: center;
            margin-top: 20px;
        }
        select {
            padding: 5px;
        }
        input[type="submit"] {
            padding: 5px 15px;
            background-color: #333;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Choose a Genre</h1>
    <form method="POST">
        <select name="selected_genre">
            <option value="">Select a Genre</option>
            {% for entry in genres %}
                <option value="{{ entry._id }}">{{ entry._id }}</option>
            {% endfor %}
        </select>
        <input type="submit" value="View Playlist">
    </form>
</body>
</html>
'''

NORESULT = '''
<!DOCTYPE html>
<html>
<head>
    <title>Raw Data</title>
>>>>>>> mongodb
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
        <a href="/"><button>Back to Raw Data</button></a>
	</div>
    <!--- Search bar --->
    <form action="/query" onsubmit="searchSongs();">
        <label for="search_query">Search:</label>
        <input type="text" id="search_query" name="search_query">
        <input type="submit" value="Submit">
    </form>
    <h2>No Results Found</h2>
    <p>No results were found for the search query: {{ search_query }}</p>
    <!-- You can add a link back to the search page if needed -->
</body>
</html>
'''
