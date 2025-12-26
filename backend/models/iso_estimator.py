def estimate_iso_rate(row):
    # Simple ISO 9223 proxy based on salinity and humidity
    # You can refine this with actual ISO equations
    base_rate = 0.5 * row["Salinity"] + 0.3 * row["Humidity"]
    modifier = 1.0 + 0.01 * row["Rainfall"] + 0.02 * row["Temperature"]
    return base_rate * modifier