from flask import Flask, request, render_template, jsonify
import urllib.request
import urllib.parse  # Import this to encode the city name
import json
from datetime import datetime

app = Flask(__name__)

# OpenWeatherMap API Key
API_KEY = '9ceb730a4d0c3fdaa32af1cff7dfe43c'

@app.route('/')
def home():
    # Render the main form to select city
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')  # Get the city from the form
    if not city:
        # If no city is selected, return an error message
        return render_template('index.html', error="Please select a city")

    # Encode the city name to handle spaces and special characters
    city_encoded = urllib.parse.quote(city)

    # Build the API request URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={API_KEY}&units=metric"
    
    try:
        # Make the request to OpenWeatherMap using urllib
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())  # Parse the JSON response
        
        # Convert sunrise and sunset from UNIX timestamp to readable format
        sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')

        # Extract weather information from the response
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"],
            "sunrise": sunrise,
            "sunset": sunset
        }

        # Render the weather information to the template
        return render_template('index.html', weather=weather_info)

    except urllib.error.HTTPError:
        # Handle the case where the city is not found or other HTTP errors
        return render_template('index.html', error="City not found or invalid API response")
    
    except Exception as e:
        # Handle other possible exceptions, like network issues
        return render_template('index.html', error=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
