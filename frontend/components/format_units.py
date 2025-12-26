import pandas as pd
import streamlit as st

def format_props_table(props: dict):
    """
    Convert raw material properties dict into a clean, display-ready DataFrame
    with proper labels and units.
    """

    # Map raw keys to display labels
    label_map = {
        "carbon": "Carbon",
        "sulphur": "Sulphur",
        "phosphorus": "Phosphorus",
        "s_plus_p": "S + P",
        "yield_strength": "Yield Strength",
        "ts_ys_ratio": "TS/YS Ratio",
        "elongation": "Elongation"
    }

    # Units for each property
    units = {
        "Carbon": "wt%",
        "Sulphur": "wt%",
        "Phosphorus": "wt%",
        "S + P": "wt%",
        "Yield Strength": "MPa",
        "TS/YS Ratio": "ratio",
        "Elongation": "%"
    }

    # Build DataFrame
    df = pd.DataFrame({
        "Property": [label_map.get(k, k) for k in props.keys()],
        "Value": list(props.values()),
        "Unit": [units.get(label_map.get(k, k), "") for k in props.keys()]
    })

    # Display in Streamlit
    st.dataframe(df)