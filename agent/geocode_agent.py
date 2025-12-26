# agent/geocode_agent.py

import requests
import os
from dotenv import load_dotenv

# Load API key from .env
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(project_root, "docs", ".env")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("WEATHER_API_KEY")

def get_coordinates(city, state=None, country="IN", limit=1):
    """Convert city name to (lat, lon) using OpenWeather Geocoding API."""
    query = f"{city},{state},{country}" if state else f"{city},{country}"
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit={limit}&appid={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError(f"No coordinates found for {city}")
    return data[0]["lat"], data[0]["lon"]

if __name__ == "__main__":
    city = "Kolkata"
    lat, lon = get_coordinates(city)
    print(f"📍 {city} → lat={lat}, lon={lon}")