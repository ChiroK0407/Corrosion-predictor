import streamlit as st

def city_and_mode_selector():
    city = st.text_input("Enter City Name", placeholder="Enter city name (e.g. Kolkata)")
    mode = st.radio("Choose Mode", ["Single Grade", "Compare All Grades"])
    grade = None
    if mode == "Single Grade":
        grade = st.selectbox("Select Rebar Grade", ["Fe415", "Fe500", "Fe500D", "Fe550", "Fe600"])
    return city, mode, grade