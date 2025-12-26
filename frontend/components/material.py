import streamlit as st
import pandas as pd

def show_material(material_props):
    df = pd.DataFrame.from_dict(material_props, orient="index", columns=["Value"])
    df.index.name = "Property"
    st.write("### 🔩 Material Properties")
    st.table(df)