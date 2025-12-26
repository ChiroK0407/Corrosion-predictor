import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
from backend.models.iso_estimator import estimate_iso_rate

def train_cecri_xgb_residual(material: str, data_path="data/cecri_materials.csv", log_transform=False):
    df = pd.read_csv(data_path)
    df = df[df["Material"] == material].dropna()

    # --- ISO baseline ---
    df["ISO_Rate"] = df.apply(estimate_iso_rate, axis=1)
    df["Residual"] = df["CorrosionRate"] - df["ISO_Rate"]

    # --- Clean invalid residuals ---
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Residual"])
    df["Residual"] = np.clip(df["Residual"], -1000, 1000)

    # --- Features ---
    X = df[["Temperature", "Humidity", "Salinity", "Rainfall"]].copy()
    X["Salinity_Humidity"] = df["Salinity"] * df["Humidity"]
    X["Rainfall_Temperature"] = df["Rainfall"] * df["Temperature"]
    X["CoastalFlag"] = (df["Salinity"] > df["Salinity"].median()).astype(int)
    X["IndustrialFlag"] = (df["Humidity"] > 70).astype(int)

    y = df["Residual"]
    if log_transform:
        y = np.log1p(y)

    # --- Train/test split ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- XGBoost model ---
    xgb = XGBRegressor(
        n_estimators=1000,
        learning_rate=0.01,
        max_depth=10,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )
    xgb.fit(X_train, y_train)

    # --- Predictions ---
    residual_pred = xgb.predict(X_test)
    if log_transform:
        residual_pred = np.expm1(residual_pred)
        y_test_eval = np.expm1(y_test)
    else:
        y_test_eval = y_test

    iso_test = df.iloc[X_test.index]["ISO_Rate"].values
    final_pred = iso_test + residual_pred
    actual_rate = df.iloc[X_test.index]["CorrosionRate"].values

    rmse = np.sqrt(mean_squared_error(actual_rate, final_pred))
    r2 = r2_score(actual_rate, final_pred)

    return {
        "model": xgb,
        "rmse": rmse,
        "r2": r2,
        "best_params": xgb.get_params(),
        "residuals": df["Residual"],   # cleaned residuals
        "features": X                  # cleaned features
    }