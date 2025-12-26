import streamlit as st

def show_cecri_intro():
    st.markdown("""
    This module explores the **archival corrosion dataset curated by CECRI (Central Electrochemical Research Institute)**.  
    It provides reported atmospheric corrosion rates for multiple materials across diverse Indian sites, collected through decades of field exposure studies.

    ### ⚙️ Technique
    - **Dataset**: CECRI’s published archival records of corrosion rates for *Carbon Steel, Zinc, Galvanized Steel, and Aluminum*.  
    - **Environmental Features**: Temperature, humidity, salinity, and rainfall measured at each site.  
    - **Benchmarking Attempt**: Models such as SVR, Random Forest, and XGBoost were trained on this dataset.  
    - **Outcome**: Despite extensive trials, the dataset proved **misfit for predictive modeling**, highlighting the limitations of legacy data.

    ### 📖 Standards & References
    - CECRI archival corrosion studies (field exposure data across India).(https://krc.cecri.res.in/ro_2008/023-2008.pdf) 
    - ISO 9223 for atmospheric corrosivity classification and guiding values.(https://www.iso.org/standard/21436.html)  
    - Indian Standards IS 456 & IS 800 for durability references in structural engineering.

    ### 🌍 Why Visualize It?
    - Even though predictive modeling was unsuccessful, **visualizing the raw CECRI data** provides valuable spatial context.  
    - It helps researchers understand **regional diversity** in atmospheric corrosivity across India.  
    - The dataset underscores the importance of **modern, high‑resolution environmental monitoring** for future corrosion prediction research.

    ---
    🔧 This page is intended as a **benchmark and historical reference**, not a predictive tool.  
    📊 It complements the API‑driven model by showing how archival data compares spatially across sites.
    """)