import streamlit as st

def show_map_intro():
    st.markdown("""
    ## 🗺️ Corrosion Map View

    This module visualizes **regional corrosion risk** by combining **environmental API data** with 
    internationally recognized standards.

    ### ⚙️ Technique
    - **Weather & Pollution Data**: Retrieved via API agents (OpenWeather, IMD, CPCB).
    - **Normalization**: Inputs such as temperature, humidity, salinity, SO₂, and PM levels are standardized.
    - **Prediction Engine**: Uses ISO 9223 classification logic (corrosivity categories C1–CX) blended with ML regression models (SVR, Random Forest, XGBoost).
    - **Visualization**: Interpolated heatmaps and scatter maps show corrosion intensity across regions.

    ### 📖 Standards & References
    - [ISO 9223:2012: Corrosion of metals and alloys — Corrosivity of atmospheres](https://www.iso.org/standard/53499.html)
    - [ISO 9224: Guiding values for corrosion rates](https://www.iso.org/standard/53500.html)

    ### 🌍 Why 12 Cities?
    - These cities represent **major climatic zones of India**: coastal (Mumbai, Chennai), industrial (Delhi, Kolkata), inland dry (Bangalore, Hyderabad), and mixed environments.
    - CECRI and ISO studies emphasize **regional diversity** in atmospheric corrosivity — hence a representative set of 12 cities provides a balanced benchmark.
    - The dataset ensures coverage of **urban, coastal, and inland** conditions, making predictions generalizable across India.

    ---
    🔧 This page helps engineers, researchers, and policymakers visualize **where corrosion risks are highest** 
    and plan mitigation strategies accordingly.
    """)