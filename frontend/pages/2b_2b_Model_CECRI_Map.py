import sys, os
# Ensure project root is on path (two levels up from /frontend/pages/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)
    
import streamlit as st
import pandas as pd

# Import modular UI components
from components.visuals import show_map
from components.geo_mask import show_masked_heatmap_c
from frontend.components.intro_cecri import show_cecri_intro

st.title("🗺️ Map View: CECRI Dataset")

# Intro text for CECRI map page
st.write("### 🗺️ CECRI Archival Corrosion Map")
show_cecri_intro()
st.info(
    "This view plots the **reported corrosion rates** from CECRI’s archival dataset directly on a map. "
    "No predictive model is applied — this is a raw visualization of legacy data."
)

# --- Material selector ---
cecri_material = st.selectbox(
    "Select Material for Map View",
    ["Carbon Steel", "Zinc", "Galvanized Steel", "Aluminum"]
)

# --- Resolution slider ---
resolution = st.slider("Interpolation Resolution (°)", min_value=0.1, max_value=1.0, value=0.25, step=0.05)

# --- Generate Map ---
if st.button("Generate CECRI Map"):
    try:
        # --- Load datasets ---
        df_mat = pd.read_csv("data/cecri_materials.csv")
        df_sites = pd.read_csv("data/cecri_sites.csv")

        # --- Filter by material ---
        df_mat = df_mat[df_mat["Material"] == cecri_material].dropna()

        # --- Merge with site metadata ---
        df_map = pd.merge(df_mat, df_sites, on=["Site", "Latitude", "Longitude"], how="left")

        # --- Show raw city points ---
        st.write("### 📍 Reported Site Points")
        df_points = df_map[["Site", "Latitude", "Longitude", "CorrosionRate"]].copy()
        df_points = df_points.rename(columns={"Site": "City"})
        show_map(df_points, cecri_material)  # helper expecting City will now work

        # --- Boundary-aware heatmap ---
        st.write("### 🧭 Boundary-Aware Heatmap")
        show_masked_heatmap_c(df_map[["Latitude", "Longitude", "CorrosionRate"]], cecri_material, resolution)

        # --- Research Disclaimer ---
        st.markdown("""
        ---
        ### 📑 Research Note
        These plots show **raw CECRI archival values**.  
        While they provide spatial context, the dataset could not be fit into viable predictive models.  
        This underscores the need for **modern, high‑resolution datasets** for reliable corrosion mapping.
        """)

        # --- Refresh Button ---
        if st.button("🔄 Refresh Map View"):
            st.rerun()  # ✅ use st.rerun() instead of experimental_rerun
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error loading CECRI map: {e}")

st.markdown("---")
st.subheader("🔀 Quick Navigation")
st.page_link("Home.py", label="🏠 Back to Home")
st.page_link("pages/2a_2a_Model_CECRI.py", label="🗺️ Back to CECRI data-driven Model Page")