import streamlit as st

def show_intro_():
    st.markdown("""
    This module predicts **atmospheric corrosion rates** for reinforcement steel grades using **live environmental data** 
    retrieved from external APIs. It blends **real-time weather and pollution inputs** with material property standards 
    to compute site-specific corrosion severity.

    ### ⚙️ Data Sources
    - **Weather API** → Temperature, humidity, rainfall, wind speed.
    - **Pollution API** → SO₂, NOₓ, PM₂.₅, salinity proxies.
    - **Material Properties** → IS 1786:2008 specifications for Fe415, Fe500, Fe500D, Fe550, Fe600.

    ### 🧮 Computational Pipeline
    1. **Input Selection**  
       - User chooses either a **city name** or **latitude/longitude**.  
       - Rebar grade is selected (single grade or comparison across all grades).
    2. **Data Retrieval**  
       - Weather and pollution parameters are fetched via APIs.  
       - Material properties are loaded from IS 1786:2008 tables.
    3. **Feature Engineering**  
       - Derived features such as *Salinity × Humidity* and *Rainfall × Temperature* are computed.  
       - Flags for **Coastal** and **Industrial** environments are added.
    4. **Corrosion Rate Estimation**  
       - A regression model combines environmental inputs with material properties.  
       - Output is expressed in **mm/year**, benchmarked against ISO 9223 corrosivity categories.
    5. **Visualization & Logging**  
       - Results are displayed as metrics and comparison charts.  
       - Records are inserted into the database for benchmarking and reproducibility.

    ### 📖 Standards & References
    - **ISO 9223**: Classification of atmospheric corrosivity.(https://www.iso.org/standard/53499.html)  
    - **ISO 9224**: Guiding values for corrosion rates.(https://www.iso.org/standard/53500.html)  
    - **IS 1786:2008**: Indian Standard for high strength deformed steel bars.(https://law.resource.org/pub/in/bis/S03/is.1786.2008.pdf)

    ---
    🔧 This page is designed for **engineers, researchers, and policymakers** who need rapid, site-specific 
    corrosion predictions using **live environmental data**.  
    📊 It complements the CECRI archival benchmark by providing a **real-time, API-driven perspective**.
    """)