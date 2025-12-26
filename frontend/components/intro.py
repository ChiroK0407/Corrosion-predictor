import streamlit as st

def show_intro():
    st.title("🔩 Corrosion Predictor Dashboard")
    st.markdown("""
    ## Welcome to the **Corrosion Intelligence Platform**
    A research-driven tool that blends **ISO 9223 standards** with **machine learning models** to estimate corrosion rates.
    """)

    st.subheader("🔧 What this app does")
    st.markdown("""
    - 🌍 Fetches weather & pollution data automatically via APIs  
    - ⚙️ Combines ISO logic + ML (SVR, Random Forest, XGBoost)  
    - 📊 Visualizes predictions with charts & maps  
    - 🏛️ Benchmarks against CECRI archival datasets  
    """)

    st.subheader("🧭 Quick Navigation")
    st.page_link("pages/1a_1a_Model_API.py", label="🌐 Go to Model 1")
    st.page_link("pages/2a_2a_Model_CECRI.py", label="🏛️ Go to Model 2")
    st.page_link("pages/1b_1b_Model_API_Map.py", label="🗺️ API Map View")
    st.page_link("pages/2b_2b_Model_CECRI_Map.py", label="📍 CECRI Map View")