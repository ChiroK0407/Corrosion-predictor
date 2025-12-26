import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

def train_cecri_xgb(material: str, data_path="data/cecri_materials.csv", log_transform=False):
    df = pd.read_csv(data_path)
    df = df[df["Material"] == material].dropna()

    # --- Features ---
    X = df[["Temperature", "Humidity", "Salinity", "Rainfall"]].copy()
    X["Salinity_Humidity"] = df["Salinity"] * df["Humidity"]
    X["Rainfall_Temperature"] = df["Rainfall"] * df["Temperature"]
    X["CoastalFlag"] = (df["Salinity"] > df["Salinity"].median()).astype(int)
    X["IndustrialFlag"] = (df["Humidity"] > 70).astype(int)

    y = df["CorrosionRate"]
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
    if log_transform:
        y_pred = np.expm1(xgb.predict(X_test))
        y_test_eval = np.expm1(y_test)
    else:
        y_pred = xgb.predict(X_test)
        y_test_eval = y_test

    rmse = np.sqrt(mean_squared_error(y_test_eval, y_pred))
    r2 = r2_score(y_test_eval, y_pred)

    return {
        "model": xgb,
        "rmse": rmse,
        "r2": r2,
        "best_params": xgb.get_params(),
        "features": X.columns.tolist()
    }

def plot_feature_importance(model, X, y, feature_names):
    result = permutation_importance(model, X, y, n_repeats=10, random_state=42)
    importances = result.importances_mean
    sorted_idx = importances.argsort()[::-1]

    fig, ax = plt.subplots()
    ax.barh([feature_names[i] for i in sorted_idx], importances[sorted_idx])
    ax.set_xlabel("Importance Score")
    ax.set_title("Feature Importance (Permutation)")
    return fig