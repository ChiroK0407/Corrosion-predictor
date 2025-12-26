# agent/batch_runner.py

import sys
import os
import time

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from agent.geocode_agent import get_coordinates
from agent.weather_agent import get_weather, get_pollution
from agent.material_agent import get_material_properties
from backend.models.corrosion_model import estimate_corrosion_rate
from database.corrosion_db import init_db, insert_record

def run_batch(cities, grades):
    init_db()
    for city in cities:
        try:
            lat, lon = get_coordinates(city)
            # Fetch once per city
            weather = get_weather(lat, lon)
            pollution = get_pollution(lat, lon)
        except Exception as e:
            print(f"❌ Failed to fetch data for {city}: {e}")
            continue

        for grade in grades:
            try:
                material_props = get_material_properties(grade)
                corrosion_rate = estimate_corrosion_rate(weather, pollution, material_props)
                insert_record(lat, lon, weather, pollution, grade, corrosion_rate)
                print(f"✅ {city} ({grade}) → {corrosion_rate} mm/year")
            except Exception as e:
                print(f"❌ Failed for {city} ({grade}): {e}")

if __name__ == "__main__":
    cities = ["Kolkata", "Mumbai", "Delhi", "Chennai", "Bangalore", "Hyderabad"]
    grades = ["Fe415", "Fe500", "Fe500D", "Fe550", "Fe600"]

    run_batch(cities, grades)