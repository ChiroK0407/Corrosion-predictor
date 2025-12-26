import sys, os
# Ensure project root is on path (two levels up from /frontend/pages/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from frontend.components.intro_cecri import show_cecri_intro

st.title("🏛️ Corrosion Prediction: Model 2 (CECRI Archival Benchmark)")

# Intro text for CECRI page
show_cecri_intro()

# Mode selection
mode = st.radio("Choose Mode", ["Single Material", "Compare All Materials"])
model_type = st.selectbox("Select Model", ["SVR", "Random Forest", "XGBoost"])
training_type = st.radio("Training Type", ["Direct ML", "Hybrid ISO+ML"])
log_transform = st.checkbox("Apply Log Transform to Corrosion Rate")

# --- Single Material Mode ---
if mode == "Single Material":
    material = st.selectbox(
        "Select Material for Training",
        ["Carbon Steel", "Zinc", "Galvanized Steel", "Aluminum"]
    )

    if st.button("Train Model"):
        try:
            # --- Train model based on selection ---
            if model_type == "SVR":
                from backend.models.c_cecri_svr import train_cecri_svr, plot_feature_importance
                result = train_cecri_svr(material, log_transform=log_transform)

            elif model_type == "Random Forest":
                from backend.models.c_random_forest import train_cecri_rf, plot_feature_importance
                result = train_cecri_rf(material, log_transform=log_transform)

            elif model_type == "XGBoost":
                if training_type == "Direct ML":
                    from backend.models.c_xgboost import train_cecri_xgb, plot_feature_importance
                    result = train_cecri_xgb(material, log_transform=log_transform)
                else:
                    from backend.models.c_xgboost_residual import train_cecri_xgb_residual, plot_feature_importance
                    result = train_cecri_xgb_residual(material, log_transform=log_transform)

            # --- Strategy selection ---
            from backend.services.c_model_selector import select_model_strategy
            strategy, message = select_model_strategy(material, result)
            st.info(message)

            # --- Display metrics ---
            st.success("✅ Model trained successfully")
            st.write(f"**RMSE:** {result['rmse']:.3f}")
            st.write(f"**R²:** {result['r2']:.3f}")
            st.write(f"**Best Params:** {result['best_params']}")

            # --- Load dataset for plotting ---
            df = pd.read_csv("data/cecri_materials.csv")
            df = df[df["Material"] == material].dropna()

            # --- Feature engineering (same as training) ---
            X = df[["Temperature", "Humidity", "Salinity", "Rainfall"]].copy()
            X["Salinity_Humidity"] = df["Salinity"] * df["Humidity"]
            X["Rainfall_Temperature"] = df["Rainfall"] * df["Temperature"]
            X["CoastalFlag"] = (df["Salinity"] > df["Salinity"].median()).astype(int)
            X["IndustrialFlag"] = (df["Humidity"] > 70).astype(int)
            y = df["CorrosionRate"]

            # --- Predictions based on strategy ---
            if strategy == "ISO":
                from backend.models.iso_estimator import estimate_iso_rate
                df["ISO_Rate"] = df.apply(estimate_iso_rate, axis=1)
                y_pred = df["ISO_Rate"]
                fig_imp = None

            elif strategy == "Hybrid":
                df["ISO_Rate"] = df.apply(estimate_iso_rate, axis=1)
                residual_pred = result["model"].predict(X)
                y_pred = df["ISO_Rate"] + residual_pred
                fig_imp = plot_feature_importance(
                    result["model"], result["features"], result["residuals"], result["features"].columns.tolist()
                )

            else:  # Direct ML
                if model_type == "SVR":
                    X_scaled = result["scaler"].transform(X)
                    y_pred = result["model"].predict(X_scaled)
                    fig_imp = plot_feature_importance(result["model"], X_scaled, y, result["features"])
                elif model_type == "Random Forest":
                    y_pred = result["model"].predict(X)
                    fig_imp = plot_feature_importance(result["model"], X, y, result["features"])
                elif model_type == "XGBoost":
                    y_pred = result["model"].predict(X)
                    fig_imp = plot_feature_importance(result["model"], X, y, result["features"])

            # --- Scatter plot ---
            fig_scatter, ax1 = plt.subplots()
            ax1.scatter(y, y_pred, alpha=0.7, edgecolors="k")
            ax1.plot([y.min(), y.max()], [y.min(), y.max()], "r--", lw=2)
            ax1.set_xlabel("Actual Corrosion Rate")
            ax1.set_ylabel("Predicted Corrosion Rate")
            ax1.set_title(f"{model_type} ({strategy}) Performance for {material}")
            fig_scatter.tight_layout()

            # --- Side-by-side layout ---
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("### 📉 Prediction Scatter Plot")
                st.pyplot(fig_scatter, clear_figure=True)
            with col2:
                if fig_imp is not None:
                    st.write("### 📊 Feature Importance")
                    st.pyplot(fig_imp, clear_figure=True)
                else:
                    st.write("### 📊 Feature Importance")
                    st.info("ISO-only strategy → no ML feature importance available.")

            # --- Research Disclaimer ---
            st.markdown("""
            ---
            ### 📑 Research Note
            Despite extensive benchmarking, the **CECRI archival dataset** could not be fit into a viable
            predictive model using SVR, Random Forest, or XGBoost.  
            This highlights the **limitations of legacy data** and reinforces the need for modern,
            high‑resolution environmental datasets for corrosion prediction research.
            """)

            # --- Refresh Button ---
            if st.button("🔄 Refresh Page"):
                st.rerun()
                st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- Compare All Materials Mode ---
elif mode == "Compare All Materials":
    materials = ["Carbon Steel", "Zinc", "Galvanized Steel", "Aluminum"]
    results = []

    if st.button("Run Comparison"):
        for mat in materials:
            try:
                if model_type == "SVR":
                    from backend.models.c_cecri_svr import train_cecri_svr
                    result = train_cecri_svr(mat, log_transform=log_transform)

                elif model_type == "Random Forest":
                    from backend.models.c_random_forest import train_cecri_rf
                    result = train_cecri_rf(mat, log_transform=log_transform)

                elif model_type == "XGBoost":
                    if training_type == "Direct ML":
                        from backend.models.c_xgboost import train_cecri_xgb
                        result = train_cecri_xgb(mat, log_transform=log_transform)
                    else:
                        from backend.models.c_xgboost_residual import train_cecri_xgb_residual
                        result = train_cecri_xgb_residual(mat, log_transform=log_transform)

                from backend.services.c_model_selector import select_model_strategy
                strategy, _ = select_model_strategy(mat, result)

                results.append({
                    "Material": mat,
                    "RMSE": round(result["rmse"], 3),
                    "R²": round(result["r2"], 3),
                    "Strategy": strategy
                })

            except Exception as e:
                results.append({
                    "Material": mat,
                    "RMSE": None,
                    "R²": None,
                    "Strategy": f"⚠️ Failed: {e}"
                })

        # --- Display results ---
        st.success("✅ Comparison complete")
        df = pd.DataFrame(results)
        st.write("### 📊 Model Comparison Across Materials")
        st.dataframe(df)

        fig = px.bar(
            df,
            x="Material",
            y="RMSE",
            text="Strategy",
            color="Material",
            title=f"{model_type} ({training_type}) RMSE Comparison"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis_title="RMSE (µm/year)", xaxis_title="Material")
        st.plotly_chart(fig, use_container_width=True)

        # --- Research Disclaimer ---
        st.markdown("""
        ---
        ### 📑 Research Note
        The **CECRI archival dataset** shows poor fit across all tested models.  
        This underscores the importance of **modern, high‑resolution datasets** for reliable corrosion prediction.
        """)

        # --- Refresh Button ---
        if st.button("🔄 Refresh Page"):
            st.rerun()
            st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("🔀 Quick Navigation")
st.page_link("Home.py", label="🏠 Back to Home")
st.page_link("pages/2b_2b_Model_CECRI_Map.py", label="🗺️ Go to Model Map View")