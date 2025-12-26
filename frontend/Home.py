import streamlit as st
from components.intro import show_intro
from components.about import show_about

st.set_page_config(page_title="Corrosion Predictor", layout="wide")

# Sidebar navigation is automatic in multipage apps
# This file serves as the landing page

st.sidebar.success("Use the sidebar to navigate between models and map views.")

# Intro page content
show_intro()

# About section
st.markdown("---")
show_about()