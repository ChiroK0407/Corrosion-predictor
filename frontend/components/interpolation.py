import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

import numpy as np
import pandas as pd

def idw_interpolation(df_points, grid_lat_range=(8, 35), grid_lon_range=(68, 90), step=0.25, power=2):
    lats = np.round(np.arange(grid_lat_range[0], grid_lat_range[1] + step, step), 4)
    lons = np.round(np.arange(grid_lon_range[0], grid_lon_range[1] + step, step), 4)

    grid_data = []
    lat_len = len(lats)
    lon_len = len(lons)
    total = lat_len * lon_len
    counter = 0

    for lat in lats:
        for lon in lons:
            distances = np.sqrt((df_points["Latitude"] - lat)**2 + (df_points["Longitude"] - lon)**2)
            distances = np.where(distances == 0, 1e-10, distances)
            weights = 1 / (distances**power)
            rate = np.sum(weights * df_points["CorrosionRate"]) / np.sum(weights)

            grid_data.append({
                "Latitude": lat,
                "Longitude": lon,
                "CorrosionRate": rate
            })

            counter += 1
            if counter % 1000 == 0:
                print(f"[IDW] {counter}/{total} points interpolated")

    return pd.DataFrame(grid_data)

def show_interpolated_map(df_points, grade, resolution=1.0):
    df_grid = idw_interpolation(df_points, step=resolution)

    fig = px.density_mapbox(
        df_grid,
        lat="Latitude",
        lon="Longitude",
        z="CorrosionRate",
        radius=25,
        center=dict(lat=22, lon=78),
        zoom=4,
        mapbox_style="carto-positron",
        color_continuous_scale="RdYlGn_r",
        opacity=0.75,
        title=f"Boundary-Aware Corrosion Heatmap ({grade}, resolution={resolution}°)"
    )

    st.plotly_chart(fig, width='stretch')