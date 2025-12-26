import datetime

# Simple in-memory cache (replace with persistent storage if needed)
cache = {}

def get_current_quarter():
    """Return the current quarter of the day (Q1–Q4)."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 6:
        return "Q1"  # Night
    elif 6 <= hour < 12:
        return "Q2"  # Morning
    elif 12 <= hour < 18:
        return "Q3"  # Afternoon
    else:
        return "Q4"  # Evening

def save_to_cache(city, lat, lon, grade, rate):
    """Save corrosion rate to cache with quarter info."""
    quarter = get_current_quarter()
    cache.setdefault(city, {})[grade] = {
        "lat": lat,
        "lon": lon,
        "rate": rate,
        "quarter": quarter,
        "timestamp": datetime.datetime.now().isoformat()
    }

def load_cached_data(city, grade):
    """Load cached corrosion rate if still valid for current quarter."""
    entry = cache.get(city, {}).get(grade)
    if entry:
        current_quarter = get_current_quarter()
        if entry["quarter"] == current_quarter:
            return entry["rate"]
    return None