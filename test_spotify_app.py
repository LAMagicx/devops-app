import unittest
from app import app, db, insert_csv_data, parse_json
import json
from pymongo import MongoClient

class TestSpotifyApp(unittest.TestCase):
    def test_insert_csv_data(self):
        # Test if insert_csv_data inserts data into the database correctly
        db.drop_collection("test_collection")  # Clean up the test collection if it exists
        insert_csv_data("Spotify_small.csv", db, "test_collection")
        data = list(db.test_collection.find())
        self.assertEqual(len(data), 100)

    def test_raw_route(self):
        # Test the '/raw' route for a valid response
        client = app.test_client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the response status is OK

    def test_genre_bar_graph_route(self):
        # Test the '/genre-bar-graph' route for a valid response
        client = app.test_client()
        response = client.get('/genre-bar-graph')
        self.assertEqual(response.status_code, 200)  # Check if the response status is OK

        # Add more test methods for other routes and functions as needed

    def test_1406_route(self):
        # Test the '/1406' route for valid sorting
        client = app.test_client()
        response = client.get('/1406?key=danceability')
        self.assertEqual(response.status_code, 200)  # Check if the response status is OK

        # Test sorting with an invalid key
        response = client.get('/1406?key=invalid_key')
        self.assertEqual(response.status_code, 200)  # Check if the response status is OK

if __name__ == '__main__':
    unittest.main()
