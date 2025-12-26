import streamlit as st

def classify_severity(rate):
    if rate > 0.5:
        return "🔴 Severe"
    elif rate > 0.2:
        return "🟠 Moderate"
    else:
        return "🟢 Low"

def show_severity(rate):
    st.success(f"Corrosion Severity: {classify_severity(rate)}")