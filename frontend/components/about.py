import streamlit as st

def show_about():
    st.title("ℹ️ About the Corrosion Predictor")

    st.markdown("""
    The **Corrosion Predictor** is a research-driven dashboard that estimates material degradation rates across diverse environments.  
    It blends **ISO 9223 standards** with **machine learning models** to deliver accurate, explainable, and location-aware predictions.
    """)

    st.subheader("🎯 Why use it?")
    st.markdown("""
    - Plan infrastructure maintenance and material selection  
    - Benchmark against CECRI archival datasets  
    - Compare corrosion risks across Indian cities  
    - Support policy and engineering decisions with transparent metrics  
    """)

    st.subheader("🧰 Key Features")
    st.markdown("""
    - Corrosion Prediction: Estimate rates for different rebar grades and materials  
    - Map View: Visualize corrosion intensity across regions  
    - CECRI Benchmark: Train and compare models against archival datasets  
    - Explainability: Feature importance plots to understand model decisions  
    """)

    st.subheader("📖 References & Standards")
    st.markdown("""
    - ISO 9223: Corrosivity of atmospheres.(https://www.iso.org/standard/21436.html)  
    - ISO 9224: Guiding values for corrosion rates. (https://www.iso.org/standard/21437.html)  
    - Indian Standard IS 1786:2008 : HIGH STRENGTH DEFORMED STEEL BARS AND WIRES FOR CONCRETE REINFORCEMENT—SPECIFICATION (Fourth Revision )(https://law.resource.org/pub/in/bis/S03/is.1786.2008.pdf")  
    - CECRI archival datasets. (https://krc.cecri.res.in/ro_2008/023-2008.pdf)  
    """)

    st.subheader("🔧 Built With")
    st.markdown("Streamlit, FastAPI, XGBoost, LangChain — powered by data science + engineering insight.")