import unittest
from app import app  # Import the Flask app from your main app module

class TestFlaskApp(unittest.TestCase):
    
    def setUp(self):
        # Creates a test client for your Flask app
        self.app = app.test_client()
        self.app.testing = True  # Enable testing mode

    def test_homepage(self):
        # Sends a GET request to the homepage and checks if it responds with a 200 status code
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_weather_route(self):
        # Test case for the weather route with a valid city
        response = self.app.post('/weather', data={'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weather in', response.data)  # Check if 'Weather in' is in the response

if __name__ == '__main__':
    unittest.main()
