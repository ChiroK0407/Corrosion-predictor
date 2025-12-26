import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

import streamlit as st
import pandas as pd

from components.visuals import show_map
from components.geo_mask import show_masked_heatmap
from frontend.components.intro_map_1 import show_map_intro
from agent.weather_agent import get_weather, get_pollution
from agent.material_agent import get_material_properties
from backend.models.corrosion_model import estimate_corrosion_rate
from database.cache_manager import load_cached_data, save_to_cache
from database.live_sites_loader import load_live_sites

st.title("🗺️ Map View: API Model")

show_map_intro()

map_grade = st.selectbox("Select Grade for Map View", ["Fe415", "Fe500", "Fe500D", "Fe550", "Fe600"])
resolution = st.slider("Interpolation Resolution (°)", min_value=0.1, max_value=1.0, value=0.25, step=0.05)

if st.button("Enter"):
    df_live = load_live_sites("data/live_cities.csv")
    map_data = []
    counter = 0
    total = len(df_live)

    progress_bar = st.progress(0)
    status_text = st.empty()

    for _, row in df_live.iterrows():
        city_name = row["City"]
        lat = row["Latitude"]
        lon = row["Longitude"]

        try:
            rate = load_cached_data(city_name, map_grade)
            if rate is None:
                weather = get_weather(lat, lon)
                pollution = get_pollution(lat, lon)
                props = get_material_properties(map_grade)
                rate = estimate_corrosion_rate(weather, pollution, props)
                save_to_cache(city_name, lat, lon, map_grade, rate)

            map_data.append({
                "City": city_name,
                "Latitude": lat,
                "Longitude": lon,
                "CorrosionRate": rate
            })

            counter += 1
            progress_bar.progress(counter / total)
            status_text.text(f"Processed {counter}/{total} cities → {city_name}: {rate:.3f} mm/year")

        except Exception as e:
            st.warning(f"Skipping {city_name}: {e}")

    progress_bar.empty()
    status_text.text("✅ Map data loaded successfully")

    if map_data:
        df_map = pd.DataFrame(map_data)
        show_map(df_map, map_grade)

        st.write("### 🧭 Boundary-Aware Heatmap")
        show_masked_heatmap(df_map, map_grade, resolution)

        if st.button("🔄 Refresh Map View"):
            st.rerun()
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("🔀 Quick Navigation")
st.page_link("Home.py", label="🏠 Back to Home")
st.page_link("pages/1a_1a_Model_API.py", label="🗺️ Back to API-driven Model Page")