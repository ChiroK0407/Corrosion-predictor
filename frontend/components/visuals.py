import streamlit as st
import plotly.express as px
import pandas as pd

def show_comparison_chart(city, results):
    df = pd.DataFrame(results)
    fig = px.bar(df, x="Grade", y="Corrosion Rate (µm/year)",
                 title=f"Corrosion Rates for {city}",
                 text="Corrosion Rate (µm/year)",
                 color="Grade")
    fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig.update_layout(yaxis_title="µm/year", xaxis_title="Rebar Grade")
    st.plotly_chart(fig, width='stretch')

def show_map(df_map, grade):
    fig_map = px.scatter_map(
        df_map,
        lat="Latitude",
        lon="Longitude",
        color="CorrosionRate",
        size="CorrosionRate",
        hover_name="City",
        hover_data=["CorrosionRate"],
        color_continuous_scale="RdYlGn_r",
        size_max=15,
        zoom=4,
        title=f"Corrosion Rates Across Indian Cities ({grade})",
        labels={"CorrosionRate": "Corrosion Rate (µm/year)"}
    )
    st.plotly_chart(fig_map, width='stretch')