# agent/weather_agent.py

import sys

import requests
import os
from dotenv import load_dotenv

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# Load .env from docs
env_path = os.path.join(project_root, "docs", ".env")
load_dotenv(dotenv_path=env_path)

from backend.models.corrosion_model import estimate_corrosion_rate
from database.corrosion_db import init_db, insert_record

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"]
    }

def get_pollution(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()["list"][0]["components"]
    return {
        "SO2": data["so2"],
        "NO2": data["no2"],
        "PM2_5": data["pm2_5"],
        "PM10": data["pm10"]
    }

if __name__ == "__main__":
    lat, lon = 22.5726, 88.3639
    weather = get_weather(lat, lon)
    pollution = get_pollution(lat, lon)

    corrosion_rate = estimate_corrosion_rate(weather, pollution, substrate_type="carbon_steel")

    print("🌦️ Weather Data:", weather)
    print("🌫️ Pollution Data:", pollution)
    print(f"🔩 Estimated Corrosion Rate: {corrosion_rate} mm/year")

    # Save to DB
    init_db()
    insert_record(lat, lon, weather, pollution, "carbon_steel", corrosion_rate)
    print("✅ Record saved to corrosion_data.db")

