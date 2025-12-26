import streamlit as st

def show_environment(weather, pollution):
    col1, col2 = st.columns(2)

    with col1:
        st.write("### 🌦️ Weather Data")
        st.metric("Temperature (°C)", weather["temperature"])
        st.metric("Humidity (%)", weather["humidity"])
        st.metric("Wind Speed (m/s)", weather["wind_speed"])
        st.metric("Condition", weather["description"].capitalize())

    with col2:
        st.write("### 🌫️ Pollution Data")
        st.metric("SO₂ (µg/m³)", pollution["SO2"])
        st.metric("NO₂ (µg/m³)", pollution["NO2"])
        st.metric("PM2.5 (µg/m³)", pollution["PM2_5"])
        st.metric("PM10 (µg/m³)", pollution["PM10"])