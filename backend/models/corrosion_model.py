# backend/models/corrosion_model.py

def estimate_corrosion_rate(weather_data, pollution_data, material_props):
    temp = weather_data["temperature"]
    humidity = weather_data["humidity"]

    SO2 = pollution_data["SO2"]
    NO2 = pollution_data["NO2"]
    PM2_5 = pollution_data["PM2_5"]
    PM10 = pollution_data["PM10"]

    # Normalize carbon % (higher carbon → slightly more corrosion prone)
    carbon_factor = 1 + (material_props["carbon"] / 0.30)

    # Strength factor: instead of zeroing out, scale between 0.7–1.0
    strength_factor = 1.0 - (material_props["yield_strength"] / 1000.0)  # Fe600 → 0.4, not 0

    # Environmental + pollution modifiers
    env_factor = (humidity / 100) * (temp / 25) * (PM2_5 / 50)
    pollution_factor = (SO2 + NO2 + PM10) / 100

    # Base corrosion rate for carbon steel
    base_rate = 0.05

    corrosion_rate = base_rate * carbon_factor * strength_factor * (1 + env_factor + pollution_factor)
    return round(corrosion_rate, 4)