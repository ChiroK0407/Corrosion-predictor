def select_model_strategy(material: str, model_results: dict, r2_threshold=0.3):
    """
    Decide whether to use ISO-only, Direct ML, or Hybrid ISO+ML
    based on material and model performance.
    """

    r2 = model_results.get("r2", None)
    rmse = model_results.get("rmse", None)

    if r2 is None or rmse is None:
        return "ISO", "⚠️ Defaulting to ISO due to missing metrics"

    # If R² is negative or very low, fallback to ISO
    if r2 < 0:
        return "ISO", f"⚠️ ML underperformed (R²={r2:.2f}) → using ISO baseline"

    # If R² is low but positive, use Hybrid
    if 0 <= r2 < r2_threshold:
        return "Hybrid", f"🔁 Using Hybrid ISO+ML (R²={r2:.2f})"

    # If R² is strong, use Direct ML
    return "ML", f"✅ ML model selected (R²={r2:.2f})"