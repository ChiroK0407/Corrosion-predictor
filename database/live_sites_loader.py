import pandas as pd

def load_live_sites(data_path="data/live_cities.csv"):
    """
    Load static lat/long for the 12 live model cities.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: City, Latitude, Longitude
    """
    df = pd.read_csv(data_path)
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    return df.dropna()