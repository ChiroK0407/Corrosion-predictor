import geopandas as gpd
import pandas as pd
import plotly.express as px
import streamlit as st
from shapely.geometry import Point
from components.interpolation import idw_interpolation

def load_india_boundary(geojson_path="data/india_boundary.geojson"):
    return gpd.read_file(geojson_path)

def filter_points_within_india(df_grid, india_shape):
    gdf = gpd.GeoDataFrame(df_grid, geometry=gpd.points_from_xy(df_grid.Longitude, df_grid.Latitude))
    gdf.set_crs(india_shape.crs, inplace=True)
    gdf_clipped = gdf[gdf.geometry.within(india_shape.unary_union)]
    return gdf_clipped.drop(columns="geometry")

def show_masked_heatmap(df_points, grade, resolution=1.0, geojson_path="data/india_boundary.geojson"):
    # Interpolate grid
    df_grid = idw_interpolation(df_points, step=resolution)

    # Clip to India boundary
    india_shape = load_india_boundary(geojson_path)
    df_clipped = filter_points_within_india(df_grid, india_shape)

    # Plot
    fig = px.density_mapbox(
        df_clipped,
        lat="Latitude",
        lon="Longitude",
        z="CorrosionRate",
        radius=10,
        center=dict(lat=22, lon=78),
        zoom=4,
        mapbox_style="carto-positron",
        color_continuous_scale="RdYlGn_r",
        title=f"Boundary-Aware Corrosion Heatmap ({grade}, resolution={resolution}°)",
        labels={"CorrosionRate": "Corrosion Rate (mm/year)"} 
    )
    st.plotly_chart(fig, width='stretch')

def show_masked_heatmap_c(df_points, grade, resolution=1.0, geojson_path="data/india_boundary.geojson"):
    # Interpolate grid
    df_grid = idw_interpolation(df_points, step=resolution)

    # Clip to India boundary
    india_shape = load_india_boundary(geojson_path)
    df_clipped = filter_points_within_india(df_grid, india_shape)

    # Plot
    fig = px.density_mapbox(
        df_clipped,
        lat="Latitude",
        lon="Longitude",
        z="CorrosionRate",
        radius=10,
        center=dict(lat=22, lon=78),
        zoom=4,
        mapbox_style="carto-positron",
        color_continuous_scale="RdYlGn_r",
        title=f"Boundary-Aware Corrosion Heatmap ({grade}, resolution={resolution}°)",
        labels={"CorrosionRate": "Corrosion Rate (µm/year)"} 
    )
    st.plotly_chart(fig, width='stretch')

