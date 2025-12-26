# agent/predict_agent.py

import sys
import os

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from agent.weather_agent import get_weather, get_pollution
from agent.material_agent import get_material_properties
from backend.models.corrosion_model import estimate_corrosion_rate
from database.corrosion_db import init_db, insert_record
from agent.geocode_agent import get_coordinates

def run_prediction(lat, lon, grade="Fe500D"):
    """Run full pipeline: weather + pollution + material + corrosion model + DB save."""

    # Fetch environment data
    weather = get_weather(lat, lon)
    pollution = get_pollution(lat, lon)

    # Fetch material properties
    material_props = get_material_properties(grade)

    # Estimate corrosion rate
    corrosion_rate = estimate_corrosion_rate(weather, pollution, substrate_type=grade)

    # Print results
    print("🌍 Site:", f"lat={lat}, lon={lon}")
    print("\n🌦️ Weather Data:")
    for k, v in weather.items():
        print(f"  {k}: {v}")

    print("\n🌫️ Pollution Data:")
    for k, v in pollution.items():
        print(f"  {k}: {v}")

    print("\n🔩 Material Properties:", grade)
    for k, v in material_props.items():
        print(f"  {k}: {v}")

    print(f"\n📈 Estimated Corrosion Rate: {corrosion_rate} mm/year")

    # Save to DB
    init_db()
    insert_record(lat, lon, weather, pollution, grade, corrosion_rate)
    print("✅ Record saved to corrosion_data.db")

if __name__ == "__main__":
    city = "Kolkata"
lat, lon = get_coordinates(city)
run_prediction(lat, lon, grade="Fe500D")
