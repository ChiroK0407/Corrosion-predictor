import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

import streamlit as st
import pandas as pd

from components.inputs import city_and_mode_selector
from components.environment import show_environment
from components.visuals import show_comparison_chart
from components.format_units import format_props_table
from components.severity import classify_severity
from agent.geocode_agent import get_coordinates
from agent.weather_agent import get_weather, get_pollution
from agent.material_agent import get_material_properties
from backend.models.corrosion_model import estimate_corrosion_rate
from database.corrosion_db import insert_record
from frontend.components.intro_model_1 import show_intro_

st.title("🌐 Corrosion Prediction: Model 1 (API-driven)")
show_intro_()

# Input Mode Toggle
input_mode = st.radio("Choose Input Mode", ["City Name", "Latitude/Longitude"])

if input_mode == "City Name":
    city, mode, grade = city_and_mode_selector()

    if st.button("Predict Corrosion"):
        if not city or city.strip() == "":
            st.error("⚠️ Please enter a valid city name before running prediction.")
        else:
            try:
                lat, lon = get_coordinates(city)
                weather = get_weather(lat, lon)
                pollution = get_pollution(lat, lon)

                st.subheader(f"📍 Site: {city} (lat={lat:.4f}, lon={lon:.4f})")
                show_environment(weather, pollution)

                if mode == "Single Grade":
                    props = get_material_properties(grade)
                    rate = estimate_corrosion_rate(weather, pollution, props)
                    insert_record(lat, lon, weather, pollution, grade, rate)

                    st.markdown("### 🧪 Material Properties (IS 1786:2008)")
                    format_props_table(props)

                    st.markdown("### 📈 Estimated Corrosion Rate")
                    st.metric(label="Corrosion Rate", value=f"{rate:.4f} mm/year")
                    st.success(f"Corrosion Severity: {classify_severity(rate)}")

                elif mode == "Compare All Grades":
                    results = []
                    for g in ["Fe415", "Fe500", "Fe500D", "Fe550", "Fe600"]:
                        props = get_material_properties(g)
                        rate = estimate_corrosion_rate(weather, pollution, props)
                        results.append({"Grade": g, "Corrosion Rate (mm/year)": rate})
                        insert_record(lat, lon, weather, pollution, g, rate)

                    show_comparison_chart(city, results)

            except Exception as e:
                st.error(f"❌ Prediction failed: {e}")

else:  # Latitude/Longitude mode
    lat = st.number_input("Enter Latitude", format="%.6f")
    lon = st.number_input("Enter Longitude", format="%.6f")
    mode = st.radio("Choose Mode", ["Single Grade", "Compare All Grades"])
    grade = None
    if mode == "Single Grade":
        grade = st.selectbox("Select Rebar Grade", ["Fe415", "Fe500", "Fe500D", "Fe550", "Fe600"])

    if st.button("Predict Corrosion"):
        if lat == 0.0 and lon == 0.0:
            st.error("⚠️ Please enter valid latitude and longitude values before running prediction.")
        else:
            try:
                weather = get_weather(lat, lon)
                pollution = get_pollution(lat, lon)

                st.subheader(f"📍 Site: lat={lat:.4f}, lon={lon:.4f}")
                show_environment(weather, pollution)

                if mode == "Single Grade":
                    props = get_material_properties(grade)
                    rate = estimate_corrosion_rate(weather, pollution, props)
                    insert_record(lat, lon, weather, pollution, grade, rate)

                    st.markdown("### 🧪 Material Properties (IS 1786:2008)")
                    format_props_table(props)

                    st.markdown("### 📈 Estimated Corrosion Rate")
                    st.metric(label="Corrosion Rate", value=f"{rate:.4f} mm/year")
                    st.success(f"Corrosion Severity: {classify_severity(rate)}")

                elif mode == "Compare All Grades":
                    results = []
                    for g in ["Fe415", "Fe500", "Fe500D", "Fe550", "Fe600"]:
                        props = get_material_properties(g)
                        rate = estimate_corrosion_rate(weather, pollution, props)
                        results.append({"Grade": g, "Corrosion Rate (mm/year)": rate})
                        insert_record(lat, lon, weather, pollution, g, rate)

                    show_comparison_chart(f"Lat={lat}, Lon={lon}", results)

            except Exception as e:
                st.error(f"❌ Prediction failed: {e}")

st.markdown("---")
st.subheader("🔀 Quick Navigation")
st.page_link("Home.py", label="🏠 Back to Home")
st.page_link("pages/1b_1b_Model_API_Map.py", label="🗺️ Go to API Map View")
