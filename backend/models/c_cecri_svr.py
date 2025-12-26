import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

def train_cecri_svr(material: str, data_path="data/cecri_materials.csv", log_transform=False):
    df = pd.read_csv(data_path)
    df = df[df["Material"] == material].dropna()

    # --- Features with engineering ---
    X = df[["Temperature", "Humidity", "Salinity", "Rainfall"]].copy()
    X["Salinity_Humidity"] = df["Salinity"] * df["Humidity"]
    X["Rainfall_Temperature"] = df["Rainfall"] * df["Temperature"]
    X["CoastalFlag"] = (df["Salinity"] > df["Salinity"].median()).astype(int)
    X["IndustrialFlag"] = (df["Humidity"] > 70).astype(int)

    y = df["CorrosionRate"]
    if log_transform:
        y = np.log1p(y)

    # --- Scale features ---
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- Train/test split ---
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # --- SVR with GridSearch ---
    param_grid = {"C": [0.1, 1, 10], "epsilon": [0.01, 0.1, 0.2], "gamma": ["scale", "auto"]}
    svr = SVR(kernel="rbf")
    grid = GridSearchCV(svr, param_grid, cv=3, scoring="neg_mean_squared_error")
    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_

    # --- Evaluation ---
    if log_transform:
        y_pred = np.expm1(best_model.predict(X_test))
        y_test_eval = np.expm1(y_test)
    else:
        y_pred = best_model.predict(X_test)
        y_test_eval = y_test

    rmse = np.sqrt(mean_squared_error(y_test_eval, y_pred))
    r2 = r2_score(y_test_eval, y_pred)

    return {
        "model": best_model,
        "scaler": scaler,
        "rmse": rmse,
        "r2": r2,
        "best_params": grid.best_params_,
        "features": X.columns.tolist()
    }

def plot_feature_importance(model, X, y, feature_names):
    """
    Compute and plot permutation feature importance for the trained SVR model.
    """
    result = permutation_importance(model, X, y, n_repeats=10, random_state=42)
    importances = result.importances_mean
    sorted_idx = importances.argsort()[::-1]

    fig, ax = plt.subplots()
    ax.barh([feature_names[i] for i in sorted_idx], importances[sorted_idx])
    ax.set_xlabel("Importance Score")
    ax.set_title("Feature Importance (Permutation)")
    return fig