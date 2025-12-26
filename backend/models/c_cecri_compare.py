import pandas as pd
from backend.models.c_cecri_svr import train_cecri_svr

def compare_cecri_models(data_path="data/cecri_materials.csv"):
    materials = ["Carbon Steel", "Zinc", "Galvanized Steel", "Aluminum"]
    results = []

    for mat in materials:
        try:
            result = train_cecri_svr(mat, data_path)
            results.append({
                "Material": mat,
                "RMSE": round(result["rmse"], 3),
                "R²": round(result["r2"], 3)
            })
        except Exception as e:
            results.append({
                "Material": mat,
                "RMSE": None,
                "R²": None
            })
            print(f"[SVR Compare] Failed for {mat}: {e}")

    return results