import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st

def show_live_clock():
    """
    Display a live clock at the top of the Streamlit interface.
    Refreshes every second using st_autorefresh.
    """
    # Refresh every 1000 ms (1 second)
    st_autorefresh(interval=1000, key="live_clock")

    # Format current time
    now = datetime.datetime.now().strftime("%A, %d %B %Y %H:%M:%S")
    st.markdown(f"## 🕒 {now}")