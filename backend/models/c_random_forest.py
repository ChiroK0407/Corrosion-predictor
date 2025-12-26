import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

def train_cecri_rf(material: str, data_path="data/cecri_materials.csv", log_transform=False):
    """
    Train a Random Forest Regressor on CECRI archival data for a given material using strong defaults.
    """

    # --- Load dataset ---
    df = pd.read_csv(data_path)
    df = df[df["Material"] == material].dropna()

    # --- Features & target ---
    X = df[["Temperature", "Humidity", "Salinity", "Rainfall"]]
    y = df["CorrosionRate"]

    if log_transform:
        y = np.log1p(y)

    # --- Train/test split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # --- Strong default RF model ---
    rf = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)

    # --- Evaluation ---
    if log_transform:
        y_pred = np.expm1(rf.predict(X_test))
        y_test_eval = np.expm1(y_test)
    else:
        y_pred = rf.predict(X_test)
        y_test_eval = y_test

    rmse = np.sqrt(mean_squared_error(y_test_eval, y_pred))
    r2 = r2_score(y_test_eval, y_pred)

    return {
        "model": rf,
        "rmse": rmse,
        "r2": r2,
        "best_params": {
            "n_estimators": 300,
            "max_depth": None,
            "min_samples_split": 2,
            "min_samples_leaf": 1
        }
    }

def plot_feature_importance(model, X, y, feature_names):
    """
    Compute and plot permutation feature importance for the trained RF model.
    """
    result = permutation_importance(model, X, y, n_repeats=10, random_state=42)
    importances = result.importances_mean
    sorted_idx = importances.argsort()[::-1]

    fig, ax = plt.subplots()
    ax.barh([feature_names[i] for i in sorted_idx], importances[sorted_idx])
    ax.set_xlabel("Importance Score")
    ax.set_title("Feature Importance (Permutation)")
    return fig