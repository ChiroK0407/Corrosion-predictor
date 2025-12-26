import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def preprocess_cecri_data(data_path="data/cecri_materials.csv", impute=True):
    """
    Preprocess CECRI archival dataset:
    - Loads CSV
    - Cleans numeric columns
    - Handles missing corrosion rates (drop or impute)
    
    Parameters
    ----------
    data_path : str
        Path to CECRI dataset CSV.
    impute : bool
        If True, imputes missing corrosion rates using RandomForest regression.
        If False, drops rows with missing corrosion rates.
    
    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with no missing corrosion rates.
    """
    # Load dataset
    df = pd.read_csv(data_path)

    # Ensure numeric types
    for col in ["Latitude", "Longitude", "Temperature", "Humidity", "Salinity", "Rainfall", "CorrosionRate"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing environmental features
    df = df.dropna(subset=["Latitude", "Longitude", "Temperature", "Humidity", "Salinity", "Rainfall"])

    if impute:
        # Train model on complete rows
        train = df.dropna(subset=["CorrosionRate"])
        X_train = train[["Temperature", "Humidity", "Salinity", "Rainfall"]]
        y_train = train["CorrosionRate"]

        model = RandomForestRegressor(n_estimators=200, random_state=42)
        model.fit(X_train, y_train)

        # Predict missing corrosion rates
        missing = df[df["CorrosionRate"].isna()]
        if not missing.empty:
            df.loc[df["CorrosionRate"].isna(), "CorrosionRate"] = model.predict(
                missing[["Temperature", "Humidity", "Salinity", "Rainfall"]]
            )
    else:
        # Drop rows with missing corrosion rates
        df = df.dropna(subset=["CorrosionRate"])

    return df